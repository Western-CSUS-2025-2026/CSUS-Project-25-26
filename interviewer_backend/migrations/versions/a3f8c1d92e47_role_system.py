"""Role system

Revision ID: a3f8c1d92e47
Revises: 33522e742cc1
Create Date: 2026-03-29 12:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a3f8c1d92e47'
down_revision = '33522e742cc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### Create role table ###
    op.create_table(
        'role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    # ### Create user_role table ###
    op.create_table(
        'user_role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
        ),
        sa.ForeignKeyConstraint(
            ['role_id'],
            ['role.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
    )

    # ### Seed initial roles ###
    op.execute(
        """
        INSERT INTO role (name, description) VALUES
        ('admin',       'Full access to all endpoints'),
        ('interviewer', 'Can manage templates and view sessions'),
        ('candidate',   'Can participate in interview sessions'),
        ('viewer',      'Read-only access')
    """
    )

    # ### Assign all existing users the interviewer role ###
    op.execute(
        """
        INSERT INTO user_role (user_id, role_id, assigned_at)
        SELECT u.id, r.id, NOW()
        FROM "user" u
        CROSS JOIN role r
        WHERE r.name = 'interviewer'
    """
    )


def downgrade():
    op.drop_table('user_role')
    op.drop_table('role')
