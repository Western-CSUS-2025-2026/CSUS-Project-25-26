"""JWT_refactoring

Revision ID: 33522e742cc1
Revises: 825037547798
Create Date: 2026-03-11 22:10:19.822810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33522e742cc1'
down_revision = '825037547798'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'refresh_session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token_hash', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash'),
    )
    op.create_index('ix_refresh_session_user_id', 'refresh_session', ['user_id'], unique=False)
    op.create_index('ix_refresh_session_expires_at', 'refresh_session', ['expires_at'], unique=False)


def downgrade():
    op.drop_index('ix_refresh_session_expires_at', table_name='refresh_session')
    op.drop_index('ix_refresh_session_user_id', table_name='refresh_session')
    op.drop_table('refresh_session')
