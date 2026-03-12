import datetime
import hashlib
import secrets
import uuid
from functools import lru_cache
from typing import Any

import jwt

from api.settings import get_settings


settings = get_settings()


def create_access_token(user_id: int, now: datetime.datetime | None = None) -> str:
    issued_at = now or datetime.datetime.now(tz=datetime.timezone.utc)
    expire_at = issued_at + datetime.timedelta(minutes=settings.ACCESS_TOKEN_TTL_MINUTES)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "jti": uuid.uuid4().hex,
        "iat": int(issued_at.timestamp()),
        "exp": int(expire_at.timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Invalid token type")
    sub = payload.get("sub")
    if sub is None:
        raise jwt.InvalidTokenError("Missing subject")
    try:
        int(sub)
    except (TypeError, ValueError) as exc:
        raise jwt.InvalidTokenError("Invalid subject") from exc
    return payload


def generate_refresh_token() -> str:
    token_length = max(settings.REFRESH_TOKEN_LENGTH, 16)
    return secrets.token_hex((token_length + 1) // 2)[:token_length]


def hash_refresh_token(token: str) -> str:
    digest = hashlib.sha256()
    digest.update(settings.JWT_SECRET.encode("utf-8"))
    digest.update(b":")
    digest.update(token.encode("utf-8"))
    return digest.hexdigest()


@lru_cache
def get_access_token_expires_in() -> int:
    return settings.ACCESS_TOKEN_TTL_MINUTES * 60


@lru_cache
def get_refresh_token_expires_in() -> int:
    return settings.REFRESH_TOKEN_TTL_DAYS * 24 * 60 * 60


def get_refresh_token_expire_date(now: datetime.datetime | None = None) -> datetime.datetime:
    current_time = now or datetime.datetime.now(tz=datetime.timezone.utc)
    return current_time + datetime.timedelta(days=settings.REFRESH_TOKEN_TTL_DAYS)
