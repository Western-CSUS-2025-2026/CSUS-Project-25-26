from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, File
from fastapi_sqlalchemy import db

from api.exceptions import ForbiddenAction
from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis
from api.schemas.models import TwelveLabsWebhookRequest
from api.schemas.base import StatusResponseModel
from api.models.db import SessionState, Session, UserSession, SessionComponent


video = APIRouter(prefix="/video", tags=["Video"])
analyzer = VideoAnalysis()


@video.post("/{session_component_id}", status_code=202)
async def upload_video(
    session_component_id: int,
    video: UploadFile = File(...),
    user_session: UserSession = Depends(Auth()),
):
    """Upload video for a session component. Uploads to TL and sets component state to indexing."""
    session_component = SessionComponent.get(session_component_id, session=db.session)
    session = session_component.session

    if session.user_id != user_session.user_id:
        raise ForbiddenAction(Session)

    index_id = analyzer.get_or_create_index(user_session.user_id, session=db.session)
    asset = analyzer.upload_asset(file=video)
    indexed_asset = analyzer.index_asset(index_id=index_id, asset_id=asset.id)

    session_component.indexed_asset_id = indexed_asset.id
    session_component.state = SessionState.INDEXING
    db.session.commit()

    return StatusResponseModel(status="Success", message="Video uploaded and indexing started")


@video.post("/webhook/twelvelabs")
async def twelvelabs_webhook(payload: TwelveLabsWebhookRequest, background_tasks: BackgroundTasks):
    indexed_asset_id = payload.indexed_asset_id
    state = (payload.state or "").lower()
    background_tasks.add_task(analyzer.process_indexed_asset, indexed_asset_id, state)
    return StatusResponseModel(status="Success", message="Received")