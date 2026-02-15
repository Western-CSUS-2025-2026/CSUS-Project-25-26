# api/routes/session.py
import random

from fastapi import APIRouter, Depends, Form
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Session, UserSession, SessionState, Template, Question, SessionComponent
from api.schemas.models import SessionCreateResponse, SessionComponentCreateResponse, SessionComponentCreateRequest
from api.settings import get_settings
from api.utils.security import Auth

session = APIRouter(prefix="/session", tags=["Session"])


@session.post("", status_code=201, response_model=SessionCreateResponse)
async def create_session(
    user_session: UserSession = Depends(Auth()),
    template_id: int = Form(...),
) -> SessionCreateResponse:
    # 1. Load template's questions (fail early if template empty or missing)
    questions = (
        Question.query(session=db.session)
        .filter(Question.template_id == template_id)
        .all()
    )
    if not questions:
        raise ObjectNotFound(Template, template_id)

    # 2. Create session (progress tracked on SessionComponent only)
    new_session = Session.create(
        session=db.session,
        user_id=user_session.user_id,
    )
    db.session.flush()

    settings = get_settings()
    count = min(settings.QUESTIONS_PER_SESSION, len(questions))
    chosen = random.sample(questions, count) # pick 3 random questions no repeat
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
        state=SessionState.PENDING.value
    )