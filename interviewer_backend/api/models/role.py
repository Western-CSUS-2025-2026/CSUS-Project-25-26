from __future__ import annotations

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel


class Role(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_roles: Mapped[list[UserRole]] = relationship(
        "UserRole", foreign_keys="UserRole.role_id", back_populates="role", cascade="all, delete"
    )


class UserRole(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"), nullable=False)
    assigned_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False
    )

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

    user = relationship("User", foreign_keys=[user_id], back_populates="user_roles")
    role: Mapped[Role] = relationship("Role", foreign_keys=[role_id], back_populates="user_roles")
