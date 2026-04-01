"""Ensure role and user_role tables exist (idempotent).

Revision ID: f8a7b6c5d4e3
Revises: b1c2d3e4f5a6
Create Date: 2026-04-01 18:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect


revision = "f8a7b6c5d4e3"
down_revision = "b1c2d3e4f5a6"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    tables = set(inspector.get_table_names())

    if "role" not in tables:
        op.create_table(
            "role",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )
        tables.add("role")

    if "user_role" not in tables:
        op.create_table(
            "user_role",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("role_id", sa.Integer(), nullable=False),
            sa.Column(
                "assigned_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            ),
            sa.ForeignKeyConstraint(["role_id"], ["role.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "role_id", name="uq_user_role"),
        )
        op.alter_column(
            "user_role",
            "assigned_at",
            server_default=None,
            existing_type=sa.DateTime(timezone=True),
            existing_nullable=False,
        )


def downgrade():
    pass
