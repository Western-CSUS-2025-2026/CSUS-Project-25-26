import datetime
from dataclasses import dataclass

import jwt
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette.requests import Request

from api.exceptions import AuthFailed
from api.settings import get_settings


settings = get_settings()


@dataclass(frozen=True)
class JwtAuthUser:
    """Identity and roles from a validated JWT"""

    user_id: int
    roles: list[str]


def mint_access_token(user_id: int, roles: list[str]) -> tuple[str, datetime.datetime]:
    """Issue a signed JWT with embedded role names"""
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    exp = now + datetime.timedelta(days=settings.SESSION_TIME_IN_DAYS)
    payload = {
        "sub": user_id,
        "roles": roles,
        "exp": exp,
        "iat": now,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token, exp


class Auth(SecurityBase):
    model = APIKey.model_construct(in_=APIKeyIn.header, name="Authorization")
    scheme_name = "bearer"
    allow_none: bool

    def __init__(self, allow_none=False) -> None:
        super().__init__()
        self.allow_none = allow_none

    def _except(self):
        raise AuthFailed("Not authorized")

    async def __call__(
        self,
        request: Request,
    ) -> JwtAuthUser | None:
        raw = request.headers.get("Authorization")
        if not raw and self.allow_none:
            return None
        if not raw:
            self._except()
        token = raw.strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
        if not token:
            self._except()
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.PyJWTError:
            self._except()
        sub = payload.get("sub")
        if sub is None:
            self._except()
        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            self._except()
        raw_roles = payload.get("roles") or []
        if not isinstance(raw_roles, list):
            self._except()
        roles = [str(r) for r in raw_roles]
        return JwtAuthUser(user_id=user_id, roles=roles)
