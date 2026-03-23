import logging
import random
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from api.exceptions import ObjectNotFound, RateLimitExceeded, SessionDeleteFailed
from api.models.db import Question, Session, SessionComponent, SessionState, Template, Video
from api.schemas.models import SessionCreateRequest, SessionCreateResponse, SessionGet, SessionsList, SessionDeleteResponse
from api.settings import get_settings
from api.utils.s3 import delete_object
from api.utils.security import Auth, AuthUser, CsrfProtect
from api.utils.session_query import get_session_options, parse_include, serialize_session


logger: logging.Logger = logging.getLogger(__name__)
session: APIRouter = APIRouter(prefix="/sessions", tags=["Sessions"])
settings = get_settings()


@session.post("", status_code=201, response_model=SessionCreateResponse)
async def create_session(
    payload: SessionCreateRequest,
    _: None = Depends(CsrfProtect()),
    current_user: AuthUser = Depends(Auth()),
) -> SessionCreateResponse:
    if settings.VIDEO_UPLOAD_LIMIT_ENABLED:
        now = datetime.now(tz=timezone.utc)
        cutoff_24h = now - timedelta(hours=24)
        cutoff_monthly = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        monthly_count = (
            db.session.query(func.count(Session.id))
            .filter(Session.user_id == current_user.user_id)
            .filter(Session.create_ts >= cutoff_monthly)
            .scalar()
            or 0
        )
        if monthly_count >= settings.VIDEO_UPLOAD_LIMIT_MONTHLY:
            next_month = (now.replace(day=1) + timedelta(days=32)).replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            next_month_str = next_month.strftime("%Y-%m-%d")
            raise RateLimitExceeded(error_msg=f"Monthly limit exceeded, please try again at {next_month_str}")

        recent_24h_count = (
            db.session.query(func.count(Session.id))
            .filter(Session.user_id == current_user.user_id)
            .filter(Session.create_ts >= cutoff_24h)
            .scalar()
            or 0
        )
        if recent_24h_count >= settings.VIDEO_UPLOAD_LIMIT:
            latest_limited_sessions = (
                Session.query(session=db.session)
                .with_entities(Session.create_ts)
                .filter(Session.user_id == current_user.user_id)
                .filter(Session.create_ts >= cutoff_24h)
                .order_by(Session.create_ts.desc())
                .limit(settings.VIDEO_UPLOAD_LIMIT)
                .subquery()
            )
            oldest_limited_ts = db.session.query(func.min(latest_limited_sessions.c.create_ts)).scalar()
            if oldest_limited_ts:
                expires_at = oldest_limited_ts + timedelta(hours=24)
                expires_at_str = expires_at.strftime("%Y-%m-%d %H:%M:%S")
                raise RateLimitExceeded(error_msg=f"Rate limit exceeded, please try again at {expires_at_str}")
            raise RateLimitExceeded(error_msg="Rate limit exceeded, please try again later")

    # 1. Load template's questions (fail early if template empty or missing)
    template_id = payload.template_id
    questions = Question.query(session=db.session).filter(Question.template_id == template_id).all()
    if not questions:
        raise ObjectNotFound(Template, template_id)

    # 2. Create session (progress tracked on SessionComponent only)
    new_session = Session.create(
        session=db.session,
        user_id=current_user.user_id,
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
    current_user: AuthUser = Depends(Auth()),
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
        .filter(Session.user_id == current_user.user_id)
        .order_by(Session.create_ts.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return SessionsList(sessions=[serialize_session(s, valid_requested) for s in sessions])


@session.delete("/{session_id}", response_model=SessionDeleteResponse)
async def delete_session(
    session_id: int,
    _: None = Depends(CsrfProtect()),
    current_user: AuthUser = Depends(Auth()),
) -> SessionDeleteResponse:

    # Load session with components and videos (for s3_keys)
    session_obj: Optional[Session] = (
        Session.query(session=db.session)
        .options(joinedload(Session.session_components).joinedload(SessionComponent.video))
        .filter(Session.id == session_id)
        .filter(Session.user_id == current_user.user_id)
        .one_or_none()
    )
    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    s3_keys = [
        sc.video.s3_key
        for sc in session_obj.session_components
        if sc.video is not None and sc.video.s3_key
    ]

    for s3_key in s3_keys:
        delete_object(s3_key)

    try:
        db.session.delete(session_obj)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise SessionDeleteFailed()

    return SessionDeleteResponse(status="deleted")


@session.get("/{session_id}", response_model=SessionGet, response_model_exclude_none=True)
async def get_session(
    session_id: int,
    current_user: AuthUser = Depends(Auth()),
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
        .filter(Session.user_id == current_user.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    return serialize_session(session_obj, valid_requested)
