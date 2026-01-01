import logging

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Session, UserSession
from api.schemas.models import (
    FeedbackGet,
    GradeGet,
    SessionObject,
    SessionsList,
    SimpleSession,
)
from api.utils.security import Auth

logger = logging.getLogger(__name__)
session = APIRouter(prefix="/sessions", tags=["Sessions"])


@session.get("", response_model=SessionsList)
async def get_user_sessions(
    user_session: UserSession = Depends(Auth()),
    length: int = Query(
        default=10, ge=1, le=100, description="Number of sessions to return"
    ),
    skip: int = Query(default=0, ge=0, description="Number of sessions to skip"),
) -> SessionsList:
    """
    Get all of a user's past sessions.

    Returns an array of all the user's sessions with the specified length.
    """
    sessions_query = (
        Session.query(session=db.session)
        .filter(Session.user_id == user_session.user_id)
        .order_by(Session.create_ts.desc())
        .offset(skip)
        .limit(length)
    )
    sessions = sessions_query.all()

    simple_sessions = [
        SimpleSession(
            id=session.id,
            state=session.state.value,
            overall_grade=session.overall_grade,
            create_ts=session.create_ts,
        )
        for session in sessions
    ]

    return SessionsList(sessions=simple_sessions)


@session.get("/{session_id}", response_model=SessionObject)
async def get_session(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
) -> SessionObject:
    """
    Get all the data about a specific session.

    Returns a Session Object with all details including grades and feedback.
    """
    session_obj: Session | None = (
        Session.query(session=db.session)
        .filter(Session.id == session_id)
        .filter(Session.user_id == user_session.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    # Build grades with feedback
    grades = []
    for grade in session_obj.grades:
        feedback = grade.feed_back
        grades.append(
            GradeGet(
                id=grade.id,
                body_language_score=grade.body_language_score,
                speech_score=grade.speech_score,
                material_score=grade.material_score,
                brevity_score=grade.brevity_score,
                overall_score=grade.overall_score,
                feed_back=FeedbackGet(
                    id=feedback.id,
                    point=feedback.point,
                    ways_to_improve=feedback.ways_to_improve,
                ),
            )
        )

    return SessionObject(
        id=session_obj.id,
        user_id=session_obj.user_id,
        video_url=session_obj.video_url,
        transcript=session_obj.transcript,
        state=session_obj.state.value,
        overall_grade=session_obj.overall_grade,
        grades=grades,
        create_ts=session_obj.create_ts,
    )
