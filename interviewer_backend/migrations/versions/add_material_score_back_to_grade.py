"""add_material_score_back_to_grade

Revision ID: 68d45e93f7f7
Revises: 0df5f40cbb29
Create Date: 2026-01-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68d45e93f7f7'
down_revision = '0df5f40cbb29'
branch_labels = None
depends_on = None


def upgrade():
    # Add material_score column back to grade table
    op.add_column('grade', sa.Column('material_score', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    # Remove material_score column
    op.drop_column('grade', 'material_score')

