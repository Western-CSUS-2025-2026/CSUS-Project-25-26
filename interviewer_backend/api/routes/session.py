import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Session, UserSession
from api.schemas.models import SessionGet, SessionsList
from api.utils.security import Auth
from api.utils.session_query import parse_include, get_session_options

logger: logging.Logger = logging.getLogger(__name__)
session: APIRouter = APIRouter(prefix="/sessions", tags=["Sessions"])


@session.get("", response_model=SessionsList, response_model_exclude_none=True)
async def get_user_sessions(
    user_session: UserSession = Depends(Auth()),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    include: Annotated[list[str], Query()] = [],
) -> SessionsList:
    """Get history of sessions. Possible include options: components, grades, feedback, videos, questions."""

    requested = parse_include(include)
    options = get_session_options(requested)

    sessions: list[Session] = (
        Session.query(session=db.session)
        .options(*options)
        .filter(Session.user_id == user_session.user_id)
        .order_by(Session.create_ts.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    for s in sessions:
        print(s)
    return SessionsList(sessions=[SessionGet.model_validate(s) for s in sessions])


@session.get("/{session_id}", response_model=SessionGet, response_model_exclude_none=True)
async def get_session(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
    include: Annotated[list[str], Query()] = [],
) -> SessionGet:
    """Get single session. Possible include options: components, grades, feedback, videos, questions."""

    requested = parse_include(include)
    options = get_session_options(requested)

    session_obj: Optional[Session] = (
        Session.query(session=db.session)
        .options(*options)
        .filter(Session.id == session_id)
        .filter(Session.user_id == user_session.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    print(session_obj)
    return SessionGet.model_validate(session_obj)
