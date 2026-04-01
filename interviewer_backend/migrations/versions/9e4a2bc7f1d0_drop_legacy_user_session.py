"""drop legacy user_session

Revision ID: 9e4a2bc7f1d0
Revises: 7c6f2e1a9d4b
Create Date: 2026-04-01 00:10:00.000000

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '9e4a2bc7f1d0'
down_revision = '7c6f2e1a9d4b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('user_session')


def downgrade():
    op.create_table(
        'user_session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires', sa.DateTime(timezone=True), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=False),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token'),
    )
