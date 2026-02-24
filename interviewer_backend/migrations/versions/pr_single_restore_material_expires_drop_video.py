"""PR single: restore material_score, add expires_at to TL index, drop video table

Revision ID: b8c9d0e1f2a3
Revises: d4e5f6a7b8c9
Create Date: 2026-02-03

Single migration for this PR:
- Add material_score back to grade (for teammate).
- Add expires_at to twelve_labs_index (store expiry, no TL retrieve each time).
- Drop unused video table (Video model removed).
"""
from alembic import op
import sqlalchemy as sa


revision = "b8c9d0e1f2a3"
down_revision = "d4e5f6a7b8c9"
branch_labels = None
depends_on = None


def upgrade():
    # 1. Restore material_score on grade
    op.add_column(
        "grade",
        sa.Column("material_score", sa.Integer(), nullable=False, server_default="0"),
    )

    # 2. Add expires_at to twelve_labs_index
    op.add_column(
        "twelve_labs_index",
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute(
        """
        UPDATE twelve_labs_index
        SET expires_at = create_ts + INTERVAL '89 days'
        WHERE expires_at IS NULL
        """
    )
    op.alter_column(
        "twelve_labs_index",
        "expires_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )

    # 3. Drop unused video table
    op.drop_table("video")


def downgrade():
    # 3. Recreate video table
    op.create_table(
        "video",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("s3_key", sa.String(), nullable=True),
        sa.Column("size_bytes", sa.Integer(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("checksum", sa.String(), nullable=True),
        sa.Column("session_component_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["session_component_id"], ["session_component.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_component_id"),
    )

    # 2. Remove expires_at from twelve_labs_index
    op.drop_column("twelve_labs_index", "expires_at")

    # 1. Remove material_score from grade
    op.drop_column("grade", "material_score")
