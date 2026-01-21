import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db
from sqlalchemy.orm import joinedload

from api.exceptions import ObjectNotFound
from api.models.db import Session, UserSession, SessionComponent
from api.schemas.models import (
    SessionGet,
    SessionsList,
)
from api.utils.security import Auth
from api.utils.session_query import parse_include, get_session_options, build_serialization_filter

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger: logging.Logger = logging.getLogger(__name__)
session: APIRouter = APIRouter(prefix="/sessions", tags=["Sessions"])


@session.get("", response_model=SessionsList)
async def get_user_sessions(
    user_session: UserSession = Depends(Auth()),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    include: Annotated[list[str], Query(description="Comma-separated: components, grades, feedback, videos")] = [
        "components",
        "grades",
        "feedback",
        "videos",
    ],
) -> SessionsList:
    """Get summarized history of user sessions."""

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

    sessions_list = SessionsList(sessions=[SessionGet.model_validate(s) for s in sessions])

    mask = {"sessions": {"__all__": build_serialization_filter(requested)}}

    filtered_data = sessions_list.model_dump(include=mask, exclude_none=True)
    return JSONResponse(content=jsonable_encoder(filtered_data))


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
