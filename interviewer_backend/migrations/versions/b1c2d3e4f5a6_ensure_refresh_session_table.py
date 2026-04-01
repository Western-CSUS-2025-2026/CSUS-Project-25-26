"""Ensure refresh_session exists (idempotent).

Revision ID: b1c2d3e4f5a6
Revises: c28a5a3f1f7d
Create Date: 2026-04-01 12:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect


revision = "b1c2d3e4f5a6"
down_revision = "c28a5a3f1f7d"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if "refresh_session" in inspector.get_table_names():
        return
    op.create_table(
        "refresh_session",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("create_ts", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_refresh_session_user_id", "refresh_session", ["user_id"], unique=False)
    op.create_index("ix_refresh_session_expires_at", "refresh_session", ["expires_at"], unique=False)


def downgrade():
    pass
