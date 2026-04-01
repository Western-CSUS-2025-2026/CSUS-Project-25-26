from dataclasses import dataclass
from secrets import compare_digest, token_hex

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.base import SecurityBase
from jwt import InvalidTokenError
from starlette.requests import Request

from api.exceptions import AuthFailed
from api.settings import get_settings
from api.utils.jwt_auth import decode_access_token


UNSAFE_HTTP_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


@dataclass(frozen=True)
class JwtAuthUser:
    """Identity and roles from a validated access JWT (no DB lookup)."""

    user_id: int
    roles: list[str]


class Auth(SecurityBase):
    _bearer = HTTPBearer(auto_error=False)
    model = _bearer.model
    scheme_name = _bearer.scheme_name
    allow_none: bool

    def __init__(self, allow_none=False) -> None:
        super().__init__()
        self.allow_none = allow_none
        self.settings = get_settings()

    def _except(self):
        raise AuthFailed("Not authorized")

    async def __call__(
        self,
        request: Request,
    ) -> JwtAuthUser | None:
        token = request.cookies.get(self.settings.ACCESS_TOKEN_COOKIE_NAME)
        if not token:
            credentials: HTTPAuthorizationCredentials | None = await self._bearer(request)
            if credentials is not None:
                token = credentials.credentials

        if not token and self.allow_none:
            return None
        if not token:
            self._except()

        try:
            payload = decode_access_token(token)
            user_id = int(payload["sub"])
            roles = payload.get("roles") or []
        except (InvalidTokenError, KeyError, TypeError, ValueError):
            self._except()
        return JwtAuthUser(user_id=user_id, roles=roles)


def generate_csrf_token() -> str:
    settings = get_settings()
    return token_hex(settings.CSRF_TOKEN_BYTES)


class CsrfProtect:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _except(self):
        raise AuthFailed("CSRF validation failed")

    async def __call__(self, request: Request) -> None:
        if request.method.upper() not in UNSAFE_HTTP_METHODS:
            return

        authorization = request.headers.get("Authorization", "")
        if authorization.lower().startswith("bearer "):
            return

        access_cookie = request.cookies.get(self.settings.ACCESS_TOKEN_COOKIE_NAME)
        refresh_cookie = request.cookies.get(self.settings.REFRESH_TOKEN_COOKIE_NAME)
        if not access_cookie and not refresh_cookie:
            return

        csrf_cookie = request.cookies.get(self.settings.CSRF_COOKIE_NAME)
        csrf_header = request.headers.get(self.settings.CSRF_HEADER_NAME)

        if not csrf_cookie or not csrf_header:
            self._except()
        if not compare_digest(csrf_cookie, csrf_header):
            self._except()
