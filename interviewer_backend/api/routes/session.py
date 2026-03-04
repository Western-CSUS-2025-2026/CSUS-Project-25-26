import logging
import random
from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound, RateLimitExceeded
from api.models.db import Question, Session, SessionComponent, SessionState, Template, UserSession
from api.schemas.models import SessionCreateRequest, SessionCreateResponse, SessionGet, SessionsList
from api.settings import get_settings
from api.utils.security import Auth
from api.utils.session_query import get_session_options, parse_include, serialize_session

from datetime import datetime, timezone, timedelta


logger: logging.Logger = logging.getLogger(__name__)
session: APIRouter = APIRouter(prefix="/sessions", tags=["Sessions"])
settings = get_settings()


@session.post("", status_code=201, response_model=SessionCreateResponse)
async def create_session(
    payload: SessionCreateRequest,
    user_session: UserSession = Depends(Auth()),
) -> SessionCreateResponse:

    now = datetime.now(tz=timezone.utc)

    recent_sessions = (
        Session.query(session=db.session)
        .filter(Session.user_id == user_session.user_id)
        .order_by(Session.create_ts.desc())
        .limit(settings.VIDEO_UPLOAD_LIMIT)
        .all()
    )

    # count how many are expired
    cutoff = now - timedelta(hours=24)
    expired_counts = sum(1 for s in recent_sessions if s.create_ts <= cutoff)

    if expired_counts == 0 and len(recent_sessions) >= settings.VIDEO_UPLOAD_LIMIT:
        oldest_session = min(recent_sessions, key=lambda s: s.create_ts)
        expires_at = oldest_session.create_ts + timedelta(hours=24)
        raise RateLimitExceeded(error_msg=f"Rate limit exceeded, please try again at {expires_at}")


    # 1. Load template's questions (fail early if template empty or missing)
    template_id = payload.template_id
    questions = Question.query(session=db.session).filter(Question.template_id == template_id).all()
    if not questions:
        raise ObjectNotFound(Template, template_id)

    # 2. Create session (progress tracked on SessionComponent only)
    new_session = Session.create(
        session=db.session,
        user_id=user_session.user_id,
        create_ts=datetime.now(tz=timezone.utc),
    )
    db.session.flush()

    count = min(settings.QUESTIONS_PER_SESSION, len(questions))
    chosen = random.sample(questions, count)  # pick 3 random questions no repeat
    for question in chosen:
        SessionComponent.create(
            session=db.session,
            session_id=new_session.id,
            question_id=question.id,
            transcript=None,
            state=SessionState.PENDING,
        )

    db.session.commit()

    return SessionCreateResponse(
        session_id=new_session.id,
    )


@session.get("", response_model=SessionsList, response_model_exclude_none=True)
async def get_user_sessions(
    user_session: UserSession = Depends(Auth()),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    include: Annotated[list[str], Query()] = [],
) -> SessionsList:
    """
    Get history of user sessions.
    Possible include options: components, grades, feedback, videos, questions
    """
    requested = parse_include(include)
    options, valid_requested = get_session_options(requested)

    sessions: list[Session] = (
        Session.query(session=db.session)
        .options(*options)
        .filter(Session.user_id == user_session.user_id)
        .order_by(Session.create_ts.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return SessionsList(sessions=[serialize_session(s, valid_requested) for s in sessions])


@session.get("/{session_id}", response_model=SessionGet, response_model_exclude_none=True)
async def get_session(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
    include: Annotated[list[str], Query()] = [],
) -> SessionGet:
    """
    Get a single user session by ID.
    Possible include options: components, grades, feedback, videos, questions
    """
    requested = parse_include(include)
    options, valid_requested = get_session_options(requested)

    session_obj: Optional[Session] = (
        Session.query(session=db.session)
        .options(*options)
        .filter(Session.id == session_id)
        .filter(Session.user_id == user_session.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    return serialize_session(session_obj, valid_requested)
