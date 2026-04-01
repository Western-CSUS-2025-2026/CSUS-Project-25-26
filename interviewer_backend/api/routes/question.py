from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from api.exceptions import ObjectInUse, ObjectNotFound
from api.models.db import Question, SessionComponent, Template
from api.schemas.models import QuestionCreate, QuestionGet, StatusResponse
from api.utils.security import Auth, AuthUser, CsrfProtect


question = APIRouter(prefix="/questions", tags=["Questions"])


@question.post("", response_model=QuestionGet)
def create_question(
    payload: QuestionCreate,
    _csrf: None = Depends(CsrfProtect()),
    _auth: AuthUser = Depends(Auth()),
) -> QuestionGet:
    db_template: Optional[Template] = Template.query(session=db.session).get(payload.template_id)

    if not db_template:
        db.session.rollback()
        raise ObjectNotFound(Template, payload.template_id)

    new_question: Question = Question(**payload.model_dump())
    db.session.add(new_question)
    db.session.flush()
    response = QuestionGet(
        id=new_question.id,
        question=new_question.question,
        template_id=new_question.template_id,
    )
    db.session.commit()

    return response


@question.get("/template/{template_id}", response_model=list[QuestionGet])
def get_questions_for_template(
    template_id: int,
    _: AuthUser = Depends(Auth()),
) -> List[QuestionGet]:
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        db.session.rollback()
        raise ObjectNotFound(Template, template_id)

    questions: List[Question] = Question.query(session=db.session).filter(Question.template_id == template_id).all()
    response = [QuestionGet.model_validate(q) for q in questions]
    db.session.rollback()
    return response


@question.delete("/{question_id}")
def delete_question(
    question_id: int,
    _csrf: None = Depends(CsrfProtect()),
    _auth: AuthUser = Depends(Auth()),
) -> StatusResponse:
    db_question: Optional[Question] = Question.query(session=db.session).get(question_id)

    if not db_question:
        db.session.rollback()
        raise ObjectNotFound(Question, question_id)

    linked_session_component = (
        SessionComponent.query(session=db.session).filter(SessionComponent.question_id == question_id).first()
    )
    if linked_session_component is not None:
        db.session.rollback()
        raise ObjectInUse(Question, question_id, SessionComponent)

    db.session.delete(db_question)
    db.session.commit()

    return StatusResponse(status="deleted")
