"""add user_id and create_ts to session

Revision ID: 0b24a728385d
Revises: bc726b00803a
Create Date: 2025-11-16 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0b24a728385d'
down_revision = 'bc726b00803a'
branch_labels = None
depends_on = None


def upgrade():
    # Add user_id column to session table
    op.add_column('session', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('session_user_id_fkey', 'session', 'user', ['user_id'], ['id'])
    
    # Add create_ts column to session table
    op.add_column('session', sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade():
    # Remove the columns we added
    op.drop_constraint('session_user_id_fkey', 'session', type_='foreignkey')
    op.drop_column('session', 'user_id')
    op.drop_column('session', 'create_ts')

