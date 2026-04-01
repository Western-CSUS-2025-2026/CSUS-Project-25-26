from __future__ import annotations

import datetime
import enum
import logging

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel


logger = logging.getLogger(__name__)


class User(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)
    salt: Mapped[str] = mapped_column(String, nullable=True)
    verification_token: Mapped[int] = mapped_column(Integer, nullable=False)
    create_ts: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False
    )
    interview_sessions: Mapped[list["Session"]] = relationship(
        "Session", foreign_keys="Session.user_id", cascade='all, delete'
    )
    twelve_labs_index: Mapped["TwelveLabsIndex"] = relationship(
        "TwelveLabsIndex",
        foreign_keys="TwelveLabsIndex.user_id",
        back_populates="user",
        uselist=False,
        cascade="all, delete",
    )
    refresh_sessions: Mapped[list["RefreshSession"]] = relationship(
        "RefreshSession",
        foreign_keys="RefreshSession.user_id",
        back_populates="user",
        cascade="all, delete",
    )


class RefreshSession(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    create_ts: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False
    )
    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="refresh_sessions",
        primaryjoin="RefreshSession.user_id==User.id",
    )


class UserMessageDelay(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    delay_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc)
    )
    user_email: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    user_ip: Mapped[str] = mapped_column(String, unique=False, nullable=False)


class Template(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    questions: Mapped[list["Question"]] = relationship(
        "Question", foreign_keys="Question.template_id", back_populates="template", cascade="all, delete"
    )
    sessions: Mapped[list["Session"]] = relationship(
        "Session", foreign_keys="Session.template_id", back_populates="template"
    )


class Question(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey("template.id"), nullable=False)
    template: Mapped[Template] = relationship(
        "Template",
        foreign_keys=[template_id],
        back_populates="questions",
        primaryjoin="Question.template_id==Template.id",
    )
    session_components: Mapped[list["SessionComponent"]] = relationship(
        "SessionComponent", foreign_keys="SessionComponent.question_id", back_populates="question"
    )


class Grade(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body_language_score: Mapped[int] = mapped_column(Integer, nullable=False)
    speech_score: Mapped[int] = mapped_column(Integer, nullable=False)
    brevity_score: Mapped[int] = mapped_column(Integer, nullable=False)
    material_score: Mapped[int] = mapped_column(Integer, nullable=False)
    session_component_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("session_component.id"), nullable=False, unique=True
    )
    session_component: Mapped["SessionComponent"] = relationship(
        "SessionComponent",
        foreign_keys=[session_component_id],
        back_populates="grade",
        primaryjoin="Grade.session_component_id==SessionComponent.id",
    )


class Feedback(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    point: Mapped[str] = mapped_column(Text, nullable=False)
    ways_to_improve: Mapped[str] = mapped_column(Text, nullable=True)
    session_component_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("session_component.id"), nullable=False, unique=True
    )
    session_component: Mapped["SessionComponent"] = relationship(
        "SessionComponent",
        foreign_keys=[session_component_id],
        back_populates="feedback",
        primaryjoin="Feedback.session_component_id==SessionComponent.id",
    )


class Video(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    s3_key: Mapped[str] = mapped_column(String, nullable=True)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    checksum: Mapped[str] = mapped_column(String, nullable=True)
    session_component_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("session_component.id"), nullable=False, unique=True
    )
    session_component: Mapped["SessionComponent"] = relationship(
        "SessionComponent",
        foreign_keys=[session_component_id],
        back_populates="video",
        primaryjoin="Video.session_component_id==SessionComponent.id",
    )


class SessionState(enum.Enum):
    """SessionComponent state; DB enum 'componentstate' (uppercase, same as sessionstate)."""

    PENDING = "PENDING"
    INDEXING = "INDEXING"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class SessionComponent(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transcript: Mapped[str] = mapped_column(Text, nullable=True)
    state: Mapped[SessionState] = mapped_column(
        Enum(SessionState, name="componentstate"),
        nullable=False,
        default=SessionState.PENDING,
    )
    indexed_asset_id: Mapped[str | None] = mapped_column(String, nullable=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("session.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"), nullable=False)
    question: Mapped[Question] = relationship(
        "Question",
        foreign_keys=[question_id],
        back_populates="session_components",
        primaryjoin="SessionComponent.question_id==Question.id",
    )
    video: Mapped[Video] = relationship(
        "Video", foreign_keys="Video.session_component_id", back_populates="session_component", cascade="all, delete"
    )
    grade: Mapped[Grade] = relationship(
        "Grade", foreign_keys="Grade.session_component_id", back_populates="session_component", cascade="all, delete"
    )
    feedback: Mapped[Feedback] = relationship(
        "Feedback",
        foreign_keys="Feedback.session_component_id",
        back_populates="session_component",
        cascade="all, delete",
    )
    session: Mapped["Session"] = relationship(
        "Session",
        foreign_keys=[session_id],
        back_populates="session_components",
        primaryjoin="SessionComponent.session_id==Session.id",
    )


class Session(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    template_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("template.id"), nullable=True)
    overall_grade: Mapped[int] = mapped_column(Integer, nullable=True)
    create_ts: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False
    )
    session_components: Mapped[list["SessionComponent"]] = relationship(
        "SessionComponent", foreign_keys="SessionComponent.session_id", back_populates="session", cascade="all, delete"
    )
    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="interview_sessions",
        primaryjoin="Session.user_id==User.id",
    )
    template: Mapped[Template | None] = relationship(
        "Template",
        foreign_keys=[template_id],
        back_populates="sessions",
        primaryjoin="Session.template_id==Template.id",
    )


class TwelveLabsIndex(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    index_id: Mapped[str] = mapped_column(String, nullable=False)
    create_ts: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="twelve_labs_index",
        primaryjoin="TwelveLabsIndex.user_id==User.id",
        uselist=False,
    )
