from fastapi import Depends, HTTPException

from api.utils.security import Auth, JwtAuthUser


def require_roles(allowed_roles: list[str]):
    auth = Auth()

    async def _check_roles(current: JwtAuthUser = Depends(auth)) -> JwtAuthUser:
        if not allowed_roles:
            return current
        if not set(current.roles).intersection(set(allowed_roles)):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {allowed_roles}",
            )
        return current

    return _check_roles
