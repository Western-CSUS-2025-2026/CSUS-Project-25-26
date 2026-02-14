"""remove_question_from_session

Revision ID: 0df5f40cbb29
Revises: c9d8e7f6a5b4
Create Date: 2026-01-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0df5f40cbb29'
down_revision = 'c9d8e7f6a5b4'
branch_labels = None
depends_on = None


def upgrade():
    # Remove question column from session table
    op.drop_column('session', 'question')


def downgrade():
    # Add question column back (nullable for backward compatibility)
    op.add_column('session', sa.Column('question', sa.Text(), nullable=True))

