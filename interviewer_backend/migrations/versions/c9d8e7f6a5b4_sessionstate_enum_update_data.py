"""sessionstate_enum_update_data

Revision ID: c9d8e7f6a5b4
Revises: 8706923a4524
Create Date: 2026-02-02 00:00:00.000000

Runs in separate transaction so new enum values from 8706923a4524 are visible.
"""
from alembic import op


revision = 'c9d8e7f6a5b4'
down_revision = '8706923a4524'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE session
        SET state = CASE
            WHEN state::text = 'PENDING' THEN 'pending'::sessionstate
            WHEN state::text = 'IN_PROGRESS' THEN 'indexing'::sessionstate
            WHEN state::text = 'COMPLETED' THEN 'completed'::sessionstate
            WHEN state::text = 'GRADED' THEN 'completed'::sessionstate
            ELSE state
        END
    """)


def downgrade():
    pass
