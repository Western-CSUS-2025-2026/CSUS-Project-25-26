"""refactor_session_remove_analysis_data

Revision ID: b0c8c90273ec
Revises: 68d45e93f7f7
Create Date: 2026-01-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0c8c90273ec'
down_revision = '68d45e93f7f7'
branch_labels = None
depends_on = None


def upgrade():
    """
    Consolidated migration for session refactoring:
    - Remove analysis_data column from session table (moved to SessionComponent relationships)
    """
    # Remove analysis_data column from session table
    # Analysis data is now stored via SessionComponent -> Grade and Feedback relationships
    op.drop_column('session', 'analysis_data')


def downgrade():
    """
    Rollback: Add analysis_data column back to session table
    """
    op.add_column('session', sa.Column('analysis_data', sa.Text(), nullable=True))

