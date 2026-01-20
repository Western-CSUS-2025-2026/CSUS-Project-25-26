"""Add interview tables

Revision ID: add_interview_tables
Revises: bc726b00803a
Create Date: 2025-01-20

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'add_interview_tables'
down_revision = 'bc726b00803a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'interview_session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('video_task_id', sa.String(), nullable=True),
        sa.Column('video_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'interview_feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interview_session_id', sa.Integer(), nullable=False),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('clarity_score', sa.Float(), nullable=True),
        sa.Column('pace_score', sa.Float(), nullable=True),
        sa.Column('filler_word_count', sa.Integer(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('eye_contact_score', sa.Float(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('suggestions', sa.Text(), nullable=True),
        sa.Column('create_ts', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['interview_session_id'], ['interview_session.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('interview_session_id'),
    )


def downgrade():
    op.drop_table('interview_feedback')
    op.drop_table('interview_session')
