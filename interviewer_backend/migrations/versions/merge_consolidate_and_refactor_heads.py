"""merge consolidate and refactor heads

Revision ID: d4e5f6a7b8c9
Revises: a7b8c9d0e1f2, b0c8c90273ec
Create Date: 2026-02-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4e5f6a7b8c9"
down_revision = ("a7b8c9d0e1f2", "b0c8c90273ec")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
