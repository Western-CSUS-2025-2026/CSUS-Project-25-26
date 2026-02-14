# api/routes/session.py
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from api.utils.security import Auth
from api.models.db import Session, UserSession, SessionState, Template, Question, SessionComponent
from api.schemas.models import SessionCreateResponse, SessionComponentCreateResponse, SessionComponentCreateRequest
from fastapi import Form, HTTPException
from api.exceptions import ObjectNotFound
import random

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
        raise HTTPException(status_code=404, detail="Template not found or has no questions")

    # 2. Create session (progress tracked on SessionComponent only)
    new_session = Session.create(
        session=db.session,
        user_id=user_session.user_id,
    )
    db.session.flush()

    # 3. Pick one (or more) at random and create session components
    chosen = random.choice(questions)
    SessionComponent.create(
        session=db.session,
        session_id=new_session.id,
        question_id=chosen.id,
        transcript=None,
        state=SessionState.PENDING
    )

    # 4. Commit once, then return
    db.session.commit()

    return SessionCreateResponse(
        session_id=new_session.id,
        state=SessionState.PENDING.value
    )