"""TL integration: componentstate, twelve_labs_index, drop video + session.state

Combines: pr_single_material_expires_drop_video, componentstate_uppercase,
tl_integration (no-op), and drops session.state / sessionstate enum.

Revision ID: 9685e61a642f
Revises: 8b5c080bab25
Create Date: 2026-02-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '9685e61a642f'
down_revision = '8b5c080bab25'
branch_labels = None
depends_on = None


def upgrade():
    # 1. ComponentState enum (uppercase) + session_component columns
    op.execute(
        "CREATE TYPE componentstate AS ENUM "
        "('PENDING', 'INDEXING', 'ANALYZING', 'COMPLETED', 'ERROR')"
    )
    op.execute(
        "ALTER TABLE session_component ADD COLUMN state componentstate "
        "NOT NULL DEFAULT 'PENDING'::componentstate"
    )
    op.add_column('session_component', sa.Column('indexed_asset_id', sa.String(), nullable=True))

    # 2. TwelveLabsIndex table
    op.create_table(
        'twelve_labs_index',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('index_id', sa.String(), nullable=False),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )

    # 3. Drop video table (replaced by TwelveLabs direct upload)
    op.drop_table('video')

    # 4. Drop session.state (unused; progress tracked on SessionComponent only)
    op.drop_column('session', 'state')
    op.execute("DROP TYPE IF EXISTS sessionstate")


def downgrade():
    # 4. Restore session.state (sessionstate type created by 461d2e, may already exist)
    op.execute(
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sessionstate') THEN "
        "CREATE TYPE sessionstate AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'GRADED'); "
        "END IF; END $$"
    )
    op.execute(
        "ALTER TABLE session ADD COLUMN state sessionstate "
        "NOT NULL DEFAULT 'PENDING'::sessionstate"
    )

    # 3. Restore video table
    op.create_table(
        'video',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('s3_key', sa.String(), nullable=True),
        sa.Column('size_bytes', sa.Integer(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('checksum', sa.String(), nullable=True),
        sa.Column('session_component_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['session_component_id'], ['session_component.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_component_id'),
    )

    # 2. Drop twelve_labs_index
    op.drop_table('twelve_labs_index')

    # 1. Drop session_component columns + componentstate enum
    op.drop_column('session_component', 'indexed_asset_id')
    op.drop_column('session_component', 'state')
    postgresql.ENUM('PENDING', 'INDEXING', 'ANALYZING', 'COMPLETED', 'ERROR', name='componentstate').drop(op.get_bind(), checkfirst=True)
