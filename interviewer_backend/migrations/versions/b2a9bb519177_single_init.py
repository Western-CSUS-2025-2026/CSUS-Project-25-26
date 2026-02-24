"""single_init

Revision ID: b2a9bb519177
Revises:
Create Date: 2026-02-23 19:27:48.987539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b2a9bb519177'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type for SessionComponent.state (raw SQL so we can ignore "already exists")
    op.execute(
        "DO $$ BEGIN CREATE TYPE sessionstate AS ENUM "
        "('pending', 'indexing', 'analyzing', 'completed', 'error'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$"
    )
    sessionstate_type = postgresql.ENUM(
        'pending', 'indexing', 'analyzing', 'completed', 'error',
        name='sessionstate',
        create_type=False,
    )

    # Tables in dependency order
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('password_hash', sa.String(), nullable=True),
        sa.Column('salt', sa.String(), nullable=True),
        sa.Column('verification_token', sa.Integer(), nullable=False),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_table(
        'user_session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('expires', sa.DateTime(timezone=True), nullable=True),
        sa.Column('token', sa.String(), nullable=True),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token'),
    )
    op.create_table(
        'user_message_delay',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('delay_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_email', sa.String(), nullable=False),
        sa.Column('user_ip', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'question',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['template_id'], ['template.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('overall_grade', sa.Integer(), nullable=True),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'session_component',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transcript', sa.Text(), nullable=True),
        sa.Column('state', sessionstate_type, nullable=False, server_default='pending'),
        sa.Column('indexed_asset_id', sa.String(), nullable=True),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'grade',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('body_language_score', sa.Integer(), nullable=False),
        sa.Column('speech_score', sa.Integer(), nullable=False),
        sa.Column('brevity_score', sa.Integer(), nullable=False),
        sa.Column('material_score', sa.Integer(), nullable=False),
        sa.Column('session_component_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['session_component_id'], ['session_component.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_component_id'),
    )
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('point', sa.Text(), nullable=False),
        sa.Column('ways_to_improve', sa.Text(), nullable=True),
        sa.Column('session_component_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['session_component_id'], ['session_component.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_component_id'),
    )
    op.create_table(
        'twelve_labs_index',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('index_id', sa.String(), nullable=False),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )


def downgrade():
    op.drop_table('twelve_labs_index')
    op.drop_table('feedback')
    op.drop_table('grade')
    op.drop_table('session_component')
    op.drop_table('session')
    op.drop_table('question')
    op.drop_table('template')
    op.drop_table('user_message_delay')
    op.drop_table('user_session')
    op.drop_table('user')
    postgresql.ENUM('pending', 'indexing', 'analyzing', 'completed', 'error', name='sessionstate').drop(op.get_bind(), checkfirst=True)
