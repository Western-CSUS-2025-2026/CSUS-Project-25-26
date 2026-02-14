"""update_sessionstate_enum

Revision ID: 8706923a4524
Revises: 08da52bb79c6
Create Date: 2026-01-07 22:24:51.230626

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '8706923a4524'
down_revision = '08da52bb79c6'
branch_labels = None
depends_on = None


def upgrade():
    # Add new lowercase enum values only. Data UPDATE is in next migration
    # (PostgreSQL: new enum values cannot be used in the same transaction).
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'pending'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'indexing'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'analyzing'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'completed'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'error'")


def downgrade():
    # Note: PostgreSQL doesn't support removing enum values easily
    # We can't revert the enum additions, but we can update data back
    # However, we need to check if the values exist first
    # For now, we'll leave the enum values in place
    pass
