import json
import logging

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_sqlalchemy import db

from api.exceptions import ForbiddenAction
from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis
from api.schemas.models import VideoAnalysisStateResponse, TwelveLabsWebhookRequest, QuestionResponseModel, FeedbackModel
from api.schemas.base import StatusResponseModel
from api.models.db import SessionState, Session, UserSession, SessionComponent, Feedback, Grade


logger = logging.getLogger(__name__)
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
async def twelvelabs_webhook(payload: TwelveLabsWebhookRequest):
    indexed_asset_id = payload.indexed_asset_id or payload.id
    state = (payload.state or payload.status or "").lower()
    session_component_to_analyze = (
        SessionComponent.query(session=db.session)
        .filter(SessionComponent.indexed_asset_id == indexed_asset_id)
        .one_or_none()
    )
    if not session_component_to_analyze:
        return StatusResponseModel(status="Success", message="Unknown asset, ignored")

    try:
        session = session_component_to_analyze.session
        if state in ("error", "failed"):
            session_component_to_analyze.state = SessionState.ERROR
            db.session.commit()
            return StatusResponseModel(status="Success", message="Received (failure recorded)")

        session_component_to_analyze.state = SessionState.ANALYZING
        db.session.flush()
        question_text = session_component_to_analyze.question.question
        result = analyzer.generate_interview_analysis(
            video_id=indexed_asset_id,
            question=question_text
        )

        data_string = result.data if hasattr(result, "data") else str(result)
        analysis_dict = json.loads(data_string)

        if "question_responses" in analysis_dict:
            our_question_text = session_component_to_analyze.question.question
            for qr in analysis_dict["question_responses"]:
                if qr.get("question", "") != our_question_text:
                    continue

                Grade.create(
                    session=db.session,
                    session_component_id=session_component_to_analyze.id,
                    body_language_score=qr.get("body_language_score", 0),
                    speech_score=qr.get("speech_score", 0),
                    brevity_score=qr.get("brevity_score", 0),
                    material_score=qr.get("material_score", 0),
                )

                feedback_data = qr.get("feedback", {})
                points_list = feedback_data.get("points", [])
                ways_list = feedback_data.get("ways_to_improve", [])
                point_str = "\n".join(points_list) if points_list else ""
                ways_str = "\n".join(ways_list) if ways_list else None

                Feedback.create(
                    session=db.session,
                    session_component_id=session_component_to_analyze.id,
                    point=point_str,
                    ways_to_improve=ways_str
                )
                db.session.flush()

                index_id = analyzer.get_or_create_index(session.user_id, session=db.session)
                transcript_text = analyzer.get_video_transcript(
                    index_id=index_id,
                    video_id=indexed_asset_id
                )

                if transcript_text:
                    session_component_to_analyze.transcript = transcript_text
                    db.session.flush()

                session_component_to_analyze.state = SessionState.COMPLETED
                break

        db.session.commit()

        return StatusResponseModel(status="Success", message="Analysis completed successfully")

    except Exception as e:
        logger.exception("Webhook analysis failed: %s", e)
        if session_component_to_analyze:
            session_component_to_analyze.state = SessionState.ERROR
        db.session.commit()
        return StatusResponseModel(status="Success", message="Received (failure recorded)")