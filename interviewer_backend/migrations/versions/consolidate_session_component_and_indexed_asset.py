"""Consolidate: remove material_score from grade + session_component state + remove session.state + indexed_asset_id on session_component

Revision ID: a7b8c9d0e1f2
Revises: c9d8e7f6a5b4
Create Date: 2026-02-03

Single migration that:
- Drops grade.material_score (folded from remove_material_score_from_grade).
- Adds session_component.state (progress tracked per component; no session.state).
- Drops session.state.
- Moves indexed_asset_id from session to session_component (Option A: keep grades/feedback when index expires).
"""
from alembic import op
import sqlalchemy as sa


revision = "a7b8c9d0e1f2"
down_revision = "c9d8e7f6a5b4"
branch_labels = None
depends_on = None


def upgrade():
    # 0. Remove material_score from grade (folded from remove_material_score_from_grade)
    op.drop_column("grade", "material_score")

    # 1. Add session_component.state (sessionstate enum, default 'pending')
    op.execute(
        "ALTER TABLE session_component ADD COLUMN state sessionstate NOT NULL DEFAULT 'pending'"
    )

    # 2. Drop session.state (progress is on SessionComponent only)
    op.drop_column("session", "state")

    # 3. Add indexed_asset_id to session_component, backfill from session, drop from session
    op.add_column(
        "session_component",
        sa.Column("indexed_asset_id", sa.String(), nullable=True),
    )
    op.execute(
        """
        UPDATE session_component sc
        SET indexed_asset_id = s.indexed_asset_id
        FROM session s
        WHERE s.id = sc.session_id AND s.indexed_asset_id IS NOT NULL
        """
    )
    op.drop_column("session", "indexed_asset_id")


def downgrade():
    # 3. Restore session.indexed_asset_id, drop from session_component
    op.add_column(
        "session",
        sa.Column("indexed_asset_id", sa.String(), nullable=True),
    )
    op.execute(
        """
        UPDATE session s
        SET indexed_asset_id = (
            SELECT sc.indexed_asset_id
            FROM session_component sc
            WHERE sc.session_id = s.id AND sc.indexed_asset_id IS NOT NULL
            LIMIT 1
        )
        """
    )
    op.drop_column("session_component", "indexed_asset_id")

    # 2. Restore session.state
    op.execute(
        "ALTER TABLE session ADD COLUMN state sessionstate NOT NULL DEFAULT 'pending'"
    )

    # 1. Drop session_component.state
    op.drop_column("session_component", "state")

    # 0. Restore grade.material_score
    op.add_column(
        "grade",
        sa.Column("material_score", sa.Integer(), nullable=False, server_default="0"),
    )
