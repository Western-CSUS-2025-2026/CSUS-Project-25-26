from functools import lru_cache
from typing import Annotated, Literal

from annotated_types import Gt
from pydantic import ConfigDict, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    DB_DSN: PostgresDsn = 'postgresql://postgres@localhost:5432/postgres'
    DB_POOL_SIZE: Annotated[int, Gt(0)] = 10
    DB_POOL_MAX_OVERFLOW: Annotated[int, Gt(-1)] = 10
    DB_POOL_TIMEOUT_SECONDS: Annotated[int, Gt(0)] = 10
    DB_POOL_RECYCLE_SECONDS: Annotated[int, Gt(0)] = 1800
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TTL_MINUTES: Annotated[int, Gt(0)] = 15
    REFRESH_TOKEN_TTL_DAYS: Annotated[int, Gt(0)] = 7
    REFRESH_TOKEN_LENGTH: Annotated[int, Gt(15)] = 64
    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    CSRF_COOKIE_NAME: str = "csrf_token"
    CSRF_HEADER_NAME: str = "X-CSRF-Token"
    CSRF_TOKEN_BYTES: Annotated[int, Gt(7)] = 32
    AUTH_COOKIE_PATH: str = "/"
    REFRESH_COOKIE_PATH: str = "/user"
    AUTH_COOKIE_DOMAIN: str | None = None
    AUTH_COOKIE_SECURE: bool = False
    AUTH_COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    ROOT_PATH: str = '/api'
    CORS_ALLOW_ORIGINS: list[str] = ["https://jobless.live", "https://api.jobless.live"]
    CORS_ALLOW_ORIGIN_REGEX: str | None = None
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: list[str] = ["Authorization", "Content-Type", "X-CSRF-Token"]
    SESSION_TIME_IN_DAYS: int = 7
    SESSION_TOUCH_INTERVAL_SECONDS: Annotated[int, Gt(0)] = 120
    MAX_ACTIVE_SESSIONS_PER_USER: Annotated[int, Gt(0)] = 256
    MAX_NAME_LENGTH: int = 32

    EMAIL: str | None = None
    APPLICATION_HOST: str = "localhost"
    EMAIL_PASS: str | None = None
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 465
    TOKEN_LENGTH: Annotated[int, Gt(8)] = 64
    ALLOWED_EMAIL_DOMAINS: list[str] = ["@uwo.ca"]
    VERIFICATION_TOKEN_TTL: int = 10

    MAX_RETRIES: int = 10
    STOP_MAX_DELAY: int = 10000
    WAIT_MIN: int = 1000
    WAIT_MAX: int = 2000

    IP_DELAY_TIME_IN_MINUTES: float = 480
    IP_DELAY_COUNT: int = 5
    EMAIL_DELAY_TIME_IN_MINUTES: float = 1
    EMAIL_DELAY_COUNT: int = 2

    TWELVE_LABS_API_KEYS: str | None = None
    TWELVE_LABS_WEBHOOK_SECRET: str | None = None  # From TL dashboard, for webhook signature verification
    TWELVE_LABS_INDEX_NAME: str = "school"
    # Index expiry: treat index as expired this many days before TL expiry to avoid edge cases
    INDEX_EXPIRY_BUFFER_DAYS: int = 1
    # Index lifetime in days when TL does not return expiry (create_ts + this - buffer = expires_at)
    INDEX_LIFETIME_DAYS: int = 90

    QUESTIONS_PER_SESSION: int = 3
    VIDEO_UPLOAD_LIMIT: int = 2
    VIDEO_UPLOAD_LIMIT_MONTHLY: int = 10
    VIDEO_UPLOAD_LIMIT_ENABLED: bool = False

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str | None = None
    S3_UPLOAD_URL_TTL: int = 300  # seconds (5 min)
    S3_READ_URL_TTL: int = 3600  # seconds (1 hour)

    METRICS_ENABLED: bool = False

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    @field_validator("AUTH_COOKIE_DOMAIN", "CORS_ALLOW_ORIGIN_REGEX", "EMAIL")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        if value == "":
            return None
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
