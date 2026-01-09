import datetime
from typing import Annotated, List, Optional

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


class VideoUploadResponse(Base):
    asset_id: str
    indexed_asset_id: str
    session_id: int

    question: str
    state: str


class TwelveLabsWebhookRequest(Base):
    indexed_asset_id: Optional[str] = None
    state: Optional[str] = None


class FeedbackModel(Base):
    points: List[str]
    ways_to_improve: List[str]


class ImproveAnswerModel(Base):
    version: str


class QuestionResponseModel(Base):
    question: str
    body_language_score: int
    speech_score: int
    brevity_score: int
    feedback: FeedbackModel
    improved_answer: ImproveAnswerModel


class TwelveLabsAnalysisModel(Base):
    question_responses: List[QuestionResponseModel]


class VideoAnalysisStateResponse(Base):
    status: str
    session_id: int
    analysis_data: AnalysisResult | TwelveLabsAnalysisModel | None = None
    error: str | None = None