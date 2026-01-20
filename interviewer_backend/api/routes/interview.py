import logging

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import InterviewFeedback, InterviewSession, UserSession
from api.schemas.base import StatusResponseModel
from api.schemas.models import InterviewFeedbackGet, InterviewSessionGet, InterviewSessionsGet
from api.utils.security import Auth
from api.utils.twelve_labs import TwelveLabsClient


logger = logging.getLogger(__name__)
interview = APIRouter(prefix="/interview", tags=["Interview"])


def process_video_and_analyze(session_id: int, question: str):
    """
    Background task to process video upload and run analysis.
    This runs after the initial upload response is returned.
    """
    from fastapi_sqlalchemy import db as async_db

    with async_db():
        session = InterviewSession.get(session_id, session=async_db.session)

        try:
            # Wait for video indexing to complete
            session.status = "processing"
            async_db.session.commit()

            video_id = TwelveLabsClient.wait_for_task(session.video_task_id)
            session.video_id = video_id
            async_db.session.commit()

            # Analyze the interview
            session.status = "analyzing"
            async_db.session.commit()

            analysis = TwelveLabsClient.analyze_interview(video_id, question)

            # Store feedback
            feedback = InterviewFeedback(
                interview_session_id=session_id,
                overall_score=analysis.get("overall_score"),
                clarity_score=analysis.get("clarity_score"),
                pace_score=analysis.get("pace_score"),
                filler_word_count=analysis.get("filler_word_count"),
                confidence_score=analysis.get("confidence_score"),
                eye_contact_score=analysis.get("eye_contact_score"),
                summary=analysis.get("summary"),
                suggestions=analysis.get("suggestions"),
            )
            async_db.session.add(feedback)
            session.status = "completed"
            async_db.session.commit()

            logger.info(f"Interview session {session_id} analysis completed")

        except Exception as e:
            logger.error(f"Failed to process interview session {session_id}: {e}")
            session.status = "failed"
            async_db.session.commit()


@interview.post("", response_model=InterviewSessionGet)
async def create_interview(
    background_tasks: BackgroundTasks,
    question: str = Form(...),
    video: UploadFile = File(...),
    user_session: UserSession = Depends(Auth()),
) -> InterviewSessionGet:
    """
    Create a new interview session by uploading a video.

    The video will be processed in the background:
    1. Upload to Twelve Labs for indexing
    2. Wait for indexing to complete
    3. Analyze for communication skills
    4. Store feedback results

    Poll GET /interview/{id} to check status and retrieve results.
    """
    # Create interview session record
    session = InterviewSession.create(
        session=db.session,
        user_id=user_session.user_id,
        question=question,
        status="uploading",
    )
    db.session.commit()

    try:
        # Start video upload to Twelve Labs
        task = TwelveLabsClient.upload_video(video.file, video.filename)
        session.video_task_id = task.id
        session.status = "uploaded"
        db.session.commit()

        # Queue background processing
        background_tasks.add_task(process_video_and_analyze, session.id, question)

        return InterviewSessionGet(
            id=session.id,
            question=session.question,
            video_id=session.video_id,
            status=session.status,
            create_ts=session.create_ts,
            feedback=None,
        )

    except Exception as e:
        session.status = "failed"
        db.session.commit()
        raise e


@interview.get("", response_model=InterviewSessionsGet)
async def list_interviews(
    user_session: UserSession = Depends(Auth()),
) -> InterviewSessionsGet:
    """
    List all interview sessions for the current user.
    """
    sessions = (
        InterviewSession.query(session=db.session)
        .filter(InterviewSession.user_id == user_session.user_id)
        .order_by(InterviewSession.create_ts.desc())
        .all()
    )

    result = []
    for session in sessions:
        feedback = None
        if session.feedback:
            feedback = InterviewFeedbackGet(
                id=session.feedback.id,
                overall_score=session.feedback.overall_score,
                clarity_score=session.feedback.clarity_score,
                pace_score=session.feedback.pace_score,
                filler_word_count=session.feedback.filler_word_count,
                confidence_score=session.feedback.confidence_score,
                eye_contact_score=session.feedback.eye_contact_score,
                summary=session.feedback.summary,
                suggestions=session.feedback.suggestions,
                create_ts=session.feedback.create_ts,
            )

        result.append(
            InterviewSessionGet(
                id=session.id,
                question=session.question,
                video_id=session.video_id,
                status=session.status,
                create_ts=session.create_ts,
                feedback=feedback,
            )
        )

    return InterviewSessionsGet(sessions=result)


@interview.get("/{session_id}", response_model=InterviewSessionGet)
async def get_interview(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
) -> InterviewSessionGet:
    """
    Get a specific interview session by ID.

    Returns the session details and feedback if analysis is complete.
    """
    session = (
        InterviewSession.query(session=db.session)
        .filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_session.user_id,
        )
        .one_or_none()
    )

    if not session:
        raise ObjectNotFound(InterviewSession, session_id)

    feedback = None
    if session.feedback:
        feedback = InterviewFeedbackGet(
            id=session.feedback.id,
            overall_score=session.feedback.overall_score,
            clarity_score=session.feedback.clarity_score,
            pace_score=session.feedback.pace_score,
            filler_word_count=session.feedback.filler_word_count,
            confidence_score=session.feedback.confidence_score,
            eye_contact_score=session.feedback.eye_contact_score,
            summary=session.feedback.summary,
            suggestions=session.feedback.suggestions,
            create_ts=session.feedback.create_ts,
        )

    return InterviewSessionGet(
        id=session.id,
        question=session.question,
        video_id=session.video_id,
        status=session.status,
        create_ts=session.create_ts,
        feedback=feedback,
    )


@interview.delete("/{session_id}", response_model=StatusResponseModel)
async def delete_interview(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
) -> StatusResponseModel:
    """
    Delete an interview session.
    """
    session = (
        InterviewSession.query(session=db.session)
        .filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_session.user_id,
        )
        .one_or_none()
    )

    if not session:
        raise ObjectNotFound(InterviewSession, session_id)

    InterviewSession.delete(session_id, session=db.session)
    db.session.commit()

    return StatusResponseModel(status="Success", message="Interview session deleted")
