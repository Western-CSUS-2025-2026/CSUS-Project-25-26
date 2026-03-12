from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from api.exceptions import ObjectNotFound
from api.models.db import Template
from api.schemas.models import StatusResponse, TemplateCreate, TemplateGet, TemplateUpdate
from api.utils.security import Auth, AuthUser


template: APIRouter = APIRouter(prefix="/templates", tags=["Templates"])


@template.post("", response_model=TemplateGet)
def create_template(
    payload: TemplateCreate,
    _: AuthUser = Depends(Auth()),
):
    new_template: Template = Template(**payload.model_dump())
    db.session.add(new_template)
    db.session.commit()

    return TemplateGet.model_validate(new_template)


@template.get("", response_model=List[TemplateGet])
def list_templates(_: AuthUser = Depends(Auth())) -> List[TemplateGet]:
    templates: List[Template] = Template.query(session=db.session).all()

    return [TemplateGet.model_validate(t) for t in templates]


@template.get("/{template_id}", response_model=TemplateGet)
def get_template(template_id: int, _: AuthUser = Depends(Auth())):
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        raise ObjectNotFound(Template, template_id)

    return TemplateGet.model_validate(db_template)


@template.put("/{template_id}", response_model=TemplateGet)
def update_template(
    template_id: int,
    payload: TemplateUpdate,
    _: AuthUser = Depends(Auth()),
) -> TemplateGet:
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        raise ObjectNotFound(Template, template_id)

    update_data: Dict[str, Any] = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_template, key, value)

    db.session.commit()

    return TemplateGet.model_validate(db_template)


@template.delete("/{template_id}")
def delete_template(template_id: int, _: AuthUser = Depends(Auth())) -> StatusResponse:
    db_template: Optional[Template] = Template.query(session=db.session).get(template_id)

    if not db_template:
        raise ObjectNotFound(Template, template_id)

    db.session.delete(db_template)
    db.session.commit()

    return StatusResponse(status="deleted")
