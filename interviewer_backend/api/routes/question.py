from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Question, Session, SessionState, Template, UserSession
from api.schemas.models import QuestionCreate, QuestionGet, SessionObject
from api.utils.security import Auth

question = APIRouter(prefix="/questions", tags=["Questions"])


@question.post("", response_model=QuestionGet)
def create_question(
    payload: QuestionCreate,
    _: UserSession = Depends(Auth),
):
    template = Template.query(session=db.session).get(payload.template_id)
    if not template:
        raise ObjectNotFound(Template, payload.template_id)

    question = Question(**payload.model_dump())
    db.session.add(question)
    db.session.commit()
    db.session.refresh(question)
    return question


@question.get("/template/{template_id}", response_model=list[QuestionGet])
def get_questions_for_template(
    template_id: int,
    _: UserSession = Depends(Auth),
):
    return (
        Question.query(session=db.session)
        .filter(Question.template_id == template_id)
        .all()
    )


@question.delete("/{question_id}")
def delete_question(question_id: int, _: UserSession = Depends(Auth)):
    question = Question.query(session=db.session).get(question_id)
    if not question:
        raise ObjectNotFound(Question, question_id)

    db.session.delete(question)
    db.session.commit()
    return {"status": "deleted"}


@question.post("", response_model=SessionObject)
def create_session(
    user_session: UserSession = Depends(Auth()),
):
    session_obj = Session(user_id=user_session.user_id)
    db.session.add(session_obj)
    db.session.commit()
    db.session.refresh(session_obj)
    return session_obj


@question.patch("/{session_id}/state")
def update_session_state(
    session_id: int,
    new_state: SessionState,
    user_session: UserSession = Depends(Auth()),
):
    session_obj = (
        Session.query(session=db.session)
        .filter(Session.id == session_id)
        .filter(Session.user_id == user_session.user_id)
        .one_or_none()
    )

    if not session_obj:
        raise ObjectNotFound(Session, session_id)

    session_obj.state = new_state
    db.session.commit()
    return {"status": "updated"}
