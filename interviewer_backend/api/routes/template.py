from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Template
from api.schemas.models import StatusResponse, TemplateCreate, TemplateGet, TemplateUpdate
from api.utils.security import Auth, AuthUser, CsrfProtect


template: APIRouter = APIRouter(prefix="/templates", tags=["Templates"])


@template.post("", response_model=TemplateGet)
def create_template(
    payload: TemplateCreate,
    _csrf: None = Depends(CsrfProtect()),
    _auth: AuthUser = Depends(Auth()),
):
    new_template: Template = Template(**payload.model_dump())
    db.session.add(new_template)
    db.session.flush()
    response = TemplateGet(
        id=new_template.id,
        job_title=new_template.job_title,
        description=new_template.description,
        is_hidden=new_template.is_hidden,
    )
    db.session.commit()

    return response


@template.get("", response_model=List[TemplateGet])
def list_templates(_: AuthUser = Depends(Auth())) -> List[TemplateGet]:
    templates: List[Template] = Template.query(session=db.session).all()
    response = [TemplateGet.model_validate(t) for t in templates]

    db.session.rollback()
    return response


@template.get("/{template_id}", response_model=TemplateGet)
def get_template(template_id: int, _: AuthUser = Depends(Auth())):
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        db.session.rollback()
        raise ObjectNotFound(Template, template_id)

    response = TemplateGet.model_validate(db_template)
    db.session.rollback()
    return response


@template.put("/{template_id}", response_model=TemplateGet)
def update_template(
    template_id: int,
    payload: TemplateUpdate,
    _csrf: None = Depends(CsrfProtect()),
    _auth: AuthUser = Depends(Auth()),
) -> TemplateGet:
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        db.session.rollback()
        raise ObjectNotFound(Template, template_id)

    update_data: Dict[str, Any] = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_template, key, value)

    response = TemplateGet(
        id=db_template.id,
        job_title=db_template.job_title,
        description=db_template.description,
        is_hidden=db_template.is_hidden,
    )
    db.session.commit()

    return response


@template.delete("/{template_id}")
def delete_template(
    template_id: int,
    _csrf: None = Depends(CsrfProtect()),
    _auth: AuthUser = Depends(Auth()),
) -> StatusResponse:
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        db.session.rollback()
        raise ObjectNotFound(Template, template_id)

    db_template.is_hidden = True
    db.session.commit()

    return StatusResponse(status="deleted")
