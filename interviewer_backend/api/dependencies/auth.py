from fastapi import Depends, HTTPException
from fastapi_sqlalchemy import db

from api.models.db import UserSession
from api.models.role import Role, UserRole
from api.utils.security import Auth


def require_roles(allowed_roles: list[str]):
    auth = Auth()

    async def _check_roles(user_session: UserSession = Depends(auth)) -> None:
        if not allowed_roles:
            return user_session

        user_role_names = {
            row.name
            for row in (
                db.session.query(Role.name)
                .join(UserRole, UserRole.role_id == Role.id)
                .filter(UserRole.user_id == user_session.user_id)
                .all()
            )
        }

        if not user_role_names.intersection(set(allowed_roles)):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {allowed_roles}",
            )

        return user_session

    return _check_roles
