import datetime

from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from fastapi_sqlalchemy import db
from starlette.requests import Request

from api.exceptions import AuthFailed
from api.models.db import UserSession
from api.settings import get_settings
from api.utils.user_session import calc_session_expire_date


settings = get_settings()


class Auth(SecurityBase):
    model = APIKey.model_construct(in_=APIKeyIn.header, name="Authorization")
    scheme_name = "token"
    allow_none: bool

    def __init__(self, allow_none=False) -> None:
        super().__init__()
        self.allow_none = allow_none

    def _except(self):
        raise AuthFailed("Not authorized")

    async def __call__(
        self,
        request: Request,
    ) -> UserSession | None:
        token = request.headers.get("Authorization")
        if not token and self.allow_none:
            return None
        if not token:
            self._except()
        user_session: UserSession = (
            UserSession.query(session=db.session).filter(UserSession.token == token).one_or_none()
        )
        if not user_session:
            self._except()
        if user_session.expired:
            self._except()
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        touch_interval = datetime.timedelta(seconds=settings.SESSION_TOUCH_INTERVAL_SECONDS)
        if now - user_session.last_activity >= touch_interval:
            user_session.last_activity = now
            user_session.expires = calc_session_expire_date(now)
            db.session.commit()
        return user_session
