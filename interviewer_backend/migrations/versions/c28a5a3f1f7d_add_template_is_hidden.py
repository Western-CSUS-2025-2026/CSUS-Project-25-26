"""add template is_hidden flag

Revision ID: c28a5a3f1f7d
Revises: 9e4a2bc7f1d0
Create Date: 2026-04-01 03:10:00.000000

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c28a5a3f1f7d'
down_revision = '9e4a2bc7f1d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('template', sa.Column('is_hidden', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.alter_column('template', 'is_hidden', server_default=None)


def downgrade():
    op.drop_column('template', 'is_hidden')
