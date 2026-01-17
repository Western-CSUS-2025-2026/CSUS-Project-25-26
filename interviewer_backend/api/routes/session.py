import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db
from sqlalchemy.orm import joinedload, Query as SQLAQuery

from api.exceptions import ObjectNotFound
from api.models.db import Session, UserSession, SessionComponent
from api.schemas.models import (
    SessionObject,
    SessionsList,
    SimpleSession,
    GradeGet,
)
from api.utils.security import Auth

logger: logging.Logger = logging.getLogger(__name__)
session: APIRouter = APIRouter(prefix="/sessions", tags=["Sessions"])


@session.get("", response_model=SessionsList)
async def get_user_sessions(
    user_session: UserSession = Depends(Auth()),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> SessionsList:
    """Get summarized history of user sessions."""
    sessions_query: SQLAQuery = (
        Session.query(session=db.session)
        .filter(Session.user_id == user_session.user_id)
        .order_by(Session.create_ts.desc())
        .offset(offset)
        .limit(limit)
    )
    sessions: list[Session] = sessions_query.all()

    return SessionsList(
        sessions=[
            SimpleSession(
                id=s.id,
                state=s.state.value,
                overall_grade=s.overall_grade,
                create_ts=s.create_ts,
            )
            for s in sessions
        ]
    )


@session.get("/{session_id}", response_model=SessionObject)
async def get_session(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
) -> SessionObject:
    session_obj: Optional[Session] = (
        Session.query(session=db.session)
        .options(
            joinedload(Session.session_components).joinedload(SessionComponent.grade),
            joinedload(Session.session_components).joinedload(SessionComponent.feedback),
            joinedload(Session.session_components).joinedload(SessionComponent.video)
        )
        .filter(Session.id == session_id)
        .filter(Session.user_id == user_session.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    grades_list: list[GradeGet] = []
    transcripts: list[str] = []

    comp: SessionComponent
    for comp in session_obj.session_components:
        if comp.transcript:
            transcripts.append(comp.transcript)

        if comp.grade:
            scores: List[int] = [
                comp.grade.body_language_score,
                comp.grade.speech_score,
                comp.grade.material_score,
                comp.grade.brevity_score
            ]
            avg: int = sum(scores) // len(scores)

            grades_list.append(
                GradeGet(
                    id=comp.grade.id,
                    body_language_score=comp.grade.body_language_score,
                    speech_score=comp.grade.speech_score,
                    material_score=comp.grade.material_score,
                    brevity_score=comp.grade.brevity_score,
                    overall_score=avg,
                    feed_back=comp.feedback
                )
            )

    return SessionObject(
        id=session_obj.id,
        user_id=session_obj.user_id,
        state=session_obj.state.value,
        overall_grade=session_obj.overall_grade,
        create_ts=session_obj.create_ts,
        grades=grades_list,
        transcript="\n".join(transcripts) if transcripts else None,
        video_url=session_obj.session_components[0].video.s3_key if (session_obj.session_components and session_obj.session_components[0].video) else None
    )
