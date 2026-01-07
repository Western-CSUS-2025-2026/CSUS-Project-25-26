import datetime
from typing import Annotated

from annotated_types import MaxLen
from pydantic import field_validator

from api.schemas.base import Base
from api.settings import get_settings

settings = get_settings()


class RegistrationInitiate(Base):
    email: Annotated[str, MaxLen(settings.MAX_NAME_LENGTH)]

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        restricted: set[str] = {
            '"',
            "#",
            "&",
            "'",
            "(",
            ")",
            "*",
            ",",
            "/",
            ";",
            "<",
            ">",
            "?",
            "[",
            "\\",
            "]",
            "^",
            "`",
            "{",
            "|",
            "}",
            "~",
            "\n",
            "\r",
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


class FeedbackGet(Base):
    id: int
    point: str
    ways_to_improve: str | None


class GradeGet(Base):
    id: int
    body_language_score: int
    speech_score: int
    material_score: int
    brevity_score: int
    overall_score: int
    feed_back: FeedbackGet


class SimpleSession(Base):
    id: int
    state: str
    overall_grade: int | None
    create_ts: datetime.datetime


class SessionObject(Base):
    id: int
    user_id: int
    video_url: str | None
    transcript: str | None
    state: str
    overall_grade: int | None
    grades: list[GradeGet]
    create_ts: datetime.datetime


class SessionsList(Base):
    sessions: list[SimpleSession]


class SessionCreate(Base):
    pass


class SessionStateUpdate(Base):
    state: str


class TemplateBase(Base):
    job_title: str
    description: str | None = None


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(Base):
    job_title: str | None = None
    description: str | None = None


class TemplateGet(TemplateBase):
    id: int


class QuestionBase(Base):
    question: str


class QuestionCreate(QuestionBase):
    template_id: int


class QuestionUpdate(Base):
    question: str | None = None


class QuestionGet(QuestionBase):
    id: int
    template_id: int


class TemplateWithQuestionsGet(TemplateGet):
    questions: list[QuestionGet]
