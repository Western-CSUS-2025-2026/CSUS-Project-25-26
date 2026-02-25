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
    session_component_id: int
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


class VideoAnalysisStateResponse(Base):
    status: str
    session_id: int
    analysis_data: QuestionResponseModel | None = None
    error: str | None = None


class SessionCreateResponse(Base):
    """Response after creating a session."""
    session_id: int


class SessionComponentCreateRequest(Base):
    """Request to add a question/component to a session."""
    question: str


class SessionComponentCreateResponse(Base):
    """Response after creating a session component."""
    session_component_id: int
    session_id: int
    question: str
    question_id: int


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


class VideoGet(Base):
    id: int
    s3_key: str | None


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


class StatusResponse(Base):
    status: str


class SessionComponentGet(Base):
    id: int
    transcript: str | None
    question_id: int
    question: QuestionGet | None = None
    grade: GradeGet | None = None
    feedback: FeedbackGet | None = None
    video: VideoGet | None = None


class SessionGet(Base):
    id: int
    user_id: int
    state: str
    overall_grade: int | None
    create_ts: datetime.datetime
    session_components: list[SessionComponentGet] | None = None


class SessionsList(Base):
    sessions: list[SessionGet]


class SessionCreate(Base):
    pass


class SessionStateUpdate(Base):
    state: str
