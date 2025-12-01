import datetime
from typing import Annotated, List

from annotated_types import MaxLen
from pydantic import Field, field_validator

from api.schemas.base import Base
from api.settings import get_settings


settings = get_settings()


class RegistrationInitiate(Base):
    email: Annotated[str, MaxLen(settings.MAX_NAME_LENGTH)]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str):
        restricted: set[str] = {
            '"',
            '#',
            '&',
            "'",
            '(',
            ')',
            '*',
            ',',
            '/',
            ';',
            '<',
            '>',
            '?',
            '[',
            '\\',
            ']',
            '^',
            '`',
            '{',
            '|',
            '}',
            '~',
            '\n',
            '\r',
        }
        if "@" not in value:
            raise ValueError()
        if set(value) & restricted:
            raise ValueError()
        if not value.endswith(tuple(settings.ALLOWED_EMAIL_DOMAINS)):
            raise ValueError()
        return value


class RegistrationVerify(RegistrationInitiate):
    first_name: Annotated[str, MaxLen(settings.MAX_NAME_LENGTH)]
    last_name: Annotated[str, MaxLen(settings.MAX_NAME_LENGTH)]
    verification_token: int
    password: str


class RegistrationVerifyCode(RegistrationInitiate):
    verification_token: int


class UserLogin(Base):
    email: Annotated[str, MaxLen(settings.MAX_NAME_LENGTH)]
    password: str


class UserSessionGet(Base):
    user_id: int
    expires: datetime.datetime
    token: str


class UserSessionsGet(Base):
    sessions: list[UserSessionGet]


class MyUserGet(Base):
    id: int
    email: str
    first_name: str
    last_name: str


class UserGet(Base):
    id: int
    username: str


class AnalysisResult(Base):
    confidence: int = Field(..., ge=1, le=10)
    clarity: int = Field(..., ge=1, le=10)
    speech_rate: int = Field(..., ge=1, le=10)
    eye_contact: int = Field(..., ge=1, le=10)
    body_language: int = Field(..., ge=1, le=10)
    voice_tone: int = Field(..., ge=1, le=10)
    relevant_to_question: int = Field(..., ge=1, le=10)
    imp_points: List[str]
    overall_summary: str
    actionable_feedback: str


class VideoAnalysisResponseModel(Base):
    status: str
    analysis_data: AnalysisResult
