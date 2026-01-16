"""update_sessionstate_enum

Revision ID: 8706923a4524
Revises: 08da52bb79c6
Create Date: 2026-01-07 22:24:51.230626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8706923a4524'
down_revision = '08da52bb79c6'
branch_labels = None
depends_on = None


def upgrade():
    # Add new lowercase enum values to sessionstate (matching code)
    # PostgreSQL requires these to be in separate transactions, but Alembic handles this
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'pending'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'indexing'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'analyzing'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'completed'")
    op.execute("ALTER TYPE sessionstate ADD VALUE IF NOT EXISTS 'error'")
    
    # Update existing data from uppercase to lowercase
    # Use text conversion workaround since new enum values need separate transaction
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
    # Note: PostgreSQL doesn't support removing enum values easily
    # We can't revert the enum additions, but we can update data back
    # However, we need to check if the values exist first
    # For now, we'll leave the enum values in place
    pass
