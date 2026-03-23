import json
import logging

import aiohttp
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi_sqlalchemy import db

from api.exceptions import ForbiddenAction
from api.metrics import observe_background_task, record_webhook_failure
from api.models.db import Session, SessionComponent, SessionState, Video
from api.schemas.base import StatusResponseModel
from api.schemas.models import PresignedURLResponse
from api.settings import get_settings
from api.utils.s3 import generate_read_url, generate_s3_key, generate_upload_url
from api.utils.s3_webhook import verify_sns_signature
from api.utils.security import Auth, AuthUser
from api.utils.twelveLabs import VideoAnalysis
from api.utils.twelvelabs_webhook import verify_twelvelabs_signature


logger = logging.getLogger(__name__)

video = APIRouter(prefix="/video", tags=["Video"])
analyzer = VideoAnalysis()
settings = get_settings()


@video.get("/{session_component_id}/upload-url", response_model=PresignedURLResponse)
async def get_upload_url(
    session_component_id: int,
    current_user: AuthUser = Depends(Auth()),
):
    """Get a presigned S3 URL to upload a video for a session component in PENDING state."""
    session_component = SessionComponent.get(session_component_id, session=db.session)
    session = session_component.session

    if session.user_id != current_user.user_id:
        raise ForbiddenAction(Session)

    if session_component.state != SessionState.PENDING:
        raise ForbiddenAction(SessionComponent)

    video_record = Video.query(session=db.session).filter(Video.session_component_id==session_component_id).one_or_none()
    if video_record and session_component.state == SessionState.PENDING:
        raise ForbiddenAction(Video)

    s3_key = generate_s3_key(session_component_id)
    url = generate_upload_url(s3_key)

    # Create Video record so the S3 webhook can look it up by s3_key
    Video.create(
        session=db.session,
        session_component_id=session_component_id,
        s3_key=s3_key,
    )
    db.session.commit()

    return PresignedURLResponse(url=url, s3_key=s3_key)


@video.get("/{session_component_id}/watch-url", response_model=PresignedURLResponse)
async def get_watch_url(
    session_component_id: int,
    current_user: AuthUser = Depends(Auth()),
):
    """Get a presigned S3 URL to watch a previously uploaded video."""
    session_component = SessionComponent.get(session_component_id, session=db.session)
    session = session_component.session

    if session.user_id != current_user.user_id:
        raise ForbiddenAction(Session)

    video_record = (
        Video.query(session=db.session).filter(Video.session_component_id == session_component_id).one_or_none()
    )
    if not video_record or not video_record.s3_key:
        raise ForbiddenAction(Video)

    url = generate_read_url(video_record.s3_key)
    return PresignedURLResponse(url=url, s3_key=video_record.s3_key)


@video.post("/webhook/s3")
async def s3_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle S3 event notifications delivered via SNS."""
    body = await request.body()
    payload = json.loads(body)

    message_type = request.headers.get("x-amz-sns-message-type", "")

    verify_sns_signature(payload, settings.TOPIC_ARN)

    # Auto-confirm SNS subscription
    if message_type == "SubscriptionConfirmation":
        subscribe_url = payload.get("SubscribeURL")
        if subscribe_url:
            async with aiohttp.ClientSession() as http_session:
                async with http_session.get(subscribe_url) as resp:
                    logger.info("SNS subscription confirmed, status=%s", resp.status)
        return StatusResponseModel(status="Success", message="Subscription confirmed")

    # Handle actual S3 event notification
    if message_type == "Notification":
        message = json.loads(payload.get("Message", "{}"))
        records = message.get("Records", [])

        for record in records:
            s3_info = record.get("s3", {})
            s3_key = s3_info.get("object", {}).get("key", "")
            size_bytes = s3_info.get("object", {}).get("size")

            if not s3_key:
                continue

            background_tasks.add_task(_process_s3_upload, s3_key, size_bytes)

    return StatusResponseModel(status="Success", message="Received")


def _process_s3_upload(s3_key: str, size_bytes: int | None):
    """Look up the Video by s3_key, start TwelveLabs indexing if component is PENDING."""
    with observe_background_task("process_s3_upload"):
        with db():
            video_record: Video | None = Video.query(session=db.session).filter(Video.s3_key == s3_key).one_or_none()
            if not video_record:
                logger.warning("S3 webhook: no Video found for s3_key=%s", s3_key)
                return

            session_component: SessionComponent = video_record.session_component
            if session_component.state != SessionState.PENDING:
                logger.info(
                    "S3 webhook: component %s already in state %s, skipping",
                    session_component.id,
                    session_component.state.value,
                )
                return

            if size_bytes is not None:
                video_record.size_bytes = size_bytes

            try:
                session: Session = session_component.session
                index_id = analyzer.get_or_create_index(session.user_id, session=db.session)

                # Generate a short-lived read URL so TwelveLabs can fetch the video from S3
                read_url = generate_read_url(s3_key)
                asset = analyzer.client.assets.create(method="url", url=read_url)
                indexed_asset = analyzer.index_asset(index_id=index_id, asset_id=asset.id)

                session_component.indexed_asset_id = indexed_asset.id
                session_component.state = SessionState.INDEXING
                db.session.commit()
            except Exception as e:
                logger.exception("S3 webhook: failed to index video for s3_key=%s", s3_key)
                record_webhook_failure(provider="s3", reason=str(e))
                session_component.state = SessionState.ERROR
                db.session.commit()


@video.post("/webhook/twelvelabs")
async def twelvelabs_webhook(request: Request, background_tasks: BackgroundTasks):
    raw_body = await request.body()
    raw_body = verify_twelvelabs_signature(raw_body, request.headers.get("TL-Signature"))
    payload = json.loads(raw_body)

    indexed_asset_id = payload["data"]["id"]
    state = (payload["data"]["status"] or "").lower()

    if state in ("error", "failed", "timeout"):
        record_webhook_failure(provider="twelvelabs", reason=state)
    background_tasks.add_task(analyzer.process_indexed_asset, indexed_asset_id, state)
    return StatusResponseModel(status="Success", message="Received")
