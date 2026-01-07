from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Template, UserSession
from api.schemas.models import (
    TemplateCreate,
    TemplateGet,
    TemplateUpdate,
)
from api.utils.security import Auth

template = APIRouter(prefix="/templates", tags=["Templates"])


@template.post("", response_model=TemplateGet)
def create_template(
    payload: TemplateCreate,
    _: UserSession = Depends(Auth),
):
    template = Template(**payload.model_dump())
    db.session.add(template)
    db.session.commit()
    db.session.refresh(template)
    return template


@template.get("", response_model=list[TemplateGet])
def list_templates(_: UserSession = Depends(Auth)):
    return Template.query(session=db.session).all()


@template.get("/{template_id}", response_model=TemplateGet)
def get_template(template_id: int, _: UserSession = Depends(Auth)):
    template = Template.query(session=db.session).get(template_id)
    if not template:
        raise ObjectNotFound(Template, template_id)
    return template


@template.put("/{template_id}", response_model=TemplateGet)
def update_template(
    template_id: int,
    payload: TemplateUpdate,
    _: UserSession = Depends(Auth),
):
    template = Template.query(session=db.session).get(template_id)
    if not template:
        raise ObjectNotFound(Template, template_id)

    for key, value in payload.model_dump().items():
        setattr(template, key, value)

    db.session.commit()
    return template


@template.delete("/{template_id}")
def delete_template(template_id: int, _: UserSession = Depends(Auth)):
    template = Template.query(session=db.session).get(template_id)
    if not template:
        raise ObjectNotFound(Template, template_id)

    db.session.delete(template)
    db.session.commit()
    return {"status": "deleted"}
