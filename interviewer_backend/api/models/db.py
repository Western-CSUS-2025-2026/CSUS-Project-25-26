from __future__ import annotations

import datetime
import logging

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.utils.user_session import calc_session_expire_date

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
    sessions: Mapped[list[UserSession]] = relationship(
        "UserSession", foreign_keys="UserSession.user_id", back_populates="user", cascade='all, delete'
    )


class UserSession(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    expires: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=calc_session_expire_date)
    token: Mapped[str] = mapped_column(String, unique=True)
    last_activity: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc)
    )
    create_ts: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc)
    )
    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="sessions",
        primaryjoin="UserSession.user_id==User.id",
    )

    @hybrid_property
    def expired(self) -> bool:
        return self.expires <= datetime.datetime.now(tz=datetime.timezone.utc)


class UserMessageDelay(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    delay_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc)
    )
    user_email: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    user_ip: Mapped[str] = mapped_column(String, unique=False, nullable=False)
