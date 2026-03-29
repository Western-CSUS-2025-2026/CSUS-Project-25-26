import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_sqlalchemy import db

from api.dependencies.auth import require_roles
from api.models.db import User, UserSession
from api.models.role import Role, UserRole
from api.schemas.models import RoleAssignBulk, UserRolesGet

logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(prefix="/users", tags=["Roles"])


@router.get("/{user_id}/roles", response_model=UserRolesGet)
async def get_user_roles(
    user_id: int,
    _: UserSession = Depends(require_roles(["admin"])),
) -> UserRolesGet:
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    roles = db.session.query(Role).join(UserRole, UserRole.role_id == Role.id).filter(UserRole.user_id == user_id).all()

    return UserRolesGet(user_id=user_id, roles=roles)


@router.post("/{user_id}/roles", response_model=UserRolesGet)
async def assign_roles(
    user_id: int,
    body: RoleAssignBulk,
    _: UserSession = Depends(require_roles(["admin"])),
) -> UserRolesGet:
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate all role_ids exist
    roles = db.session.query(Role).filter(Role.id.in_(body.role_ids)).all()
    if len(roles) != len(body.role_ids):
        raise HTTPException(status_code=404, detail="One or more roles not found")

    # Get already assigned role_ids to avoid duplicate constraint violation
    existing_role_ids = {
        row.role_id for row in db.session.query(UserRole.role_id).filter(UserRole.user_id == user_id).all()
    }

    new_user_roles = [
        UserRole(user_id=user_id, role_id=role_id) for role_id in body.role_ids if role_id not in existing_role_ids
    ]

    db.session.add_all(new_user_roles)
    db.session.commit()

    # Return updated full role list for this user
    all_roles = (
        db.session.query(Role).join(UserRole, UserRole.role_id == Role.id).filter(UserRole.user_id == user_id).all()
    )

    return UserRolesGet(user_id=user_id, roles=all_roles)


@router.delete("/{user_id}/roles/{role_id}", response_model=UserRolesGet)
async def remove_role(
    user_id: int,
    role_id: int,
    _: UserSession = Depends(require_roles(["admin"])),
) -> UserRolesGet:
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_role = db.session.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="Role not assigned to this user")

    db.session.delete(user_role)
    db.session.commit()

    remaining_roles = (
        db.session.query(Role).join(UserRole, UserRole.role_id == Role.id).filter(UserRole.user_id == user_id).all()
    )

    return UserRolesGet(user_id=user_id, roles=remaining_roles)
