import logging
from typing import Optional, Set

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db
from sqlalchemy.orm import joinedload, Query as SQLAQuery

from api.exceptions import ObjectNotFound
from api.models.db import Session, UserSession, SessionComponent
from api.schemas.models import (
    SessionGet,
    SessionsList,
)
from api.utils.security import Auth

logger: logging.Logger = logging.getLogger(__name__)
session: APIRouter = APIRouter(prefix="/sessions", tags=["Sessions"])


def get_session_options(include: str | None):
    """
    Helper to convert a comma-separated string into SQLAlchemy joinedload options.
    """
    options = []
    if not include:
        return options

    requested: Set[str] = {i.strip().lower() for i in include.split(",")}
    print(requested)

    component_triggers = {"components", "grades", "grade", "feedback", "videos", "video"}

    if any(item in requested for item in component_triggers):
        base_load = joinedload(Session.session_components)

        if "grades" in requested:
            options.append(base_load.joinedload(SessionComponent.grade))
        if "feedback" in requested:
            options.append(base_load.joinedload(SessionComponent.feedback))
        if "videos" in requested:
            options.append(base_load.joinedload(SessionComponent.video))

        if not options:
            options.append(base_load)

    return options


@session.get("", response_model=SessionsList)
async def get_user_sessions(
    user_session: UserSession = Depends(Auth()),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    include: Optional[str] = Query(default=None, description="Comma-separated: components, grades, feedback, videos"),
) -> SessionsList:
    """Get summarized history of user sessions."""

    options = get_session_options(include)

    sessions_query: SQLAQuery = (
        Session.query(session=db.session)
        .options(*options)
        .filter(Session.user_id == user_session.user_id)
        .order_by(Session.create_ts.desc())
        .offset(offset)
        .limit(limit)
    )
    sessions: list[Session] = sessions_query.all()

    return SessionsList(sessions=[SessionGet.model_validate(s) for s in sessions])


@session.get("/{session_id}", response_model=SessionGet)
async def get_session(
    session_id: int,
    user_session: UserSession = Depends(Auth()),
) -> SessionGet:
    session_obj: Optional[Session] = (
        Session.query(session=db.session)
        .options(
            joinedload(Session.session_components).joinedload(SessionComponent.grade),
            joinedload(Session.session_components).joinedload(SessionComponent.feedback),
            joinedload(Session.session_components).joinedload(SessionComponent.video),
        )
        .filter(Session.id == session_id)
        .filter(Session.user_id == user_session.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    return SessionGet.model_validate(session_obj)
