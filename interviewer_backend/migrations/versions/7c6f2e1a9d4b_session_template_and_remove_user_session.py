"""session template link

Revision ID: 7c6f2e1a9d4b
Revises: 33522e742cc1
Create Date: 2026-04-01 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '7c6f2e1a9d4b'
down_revision = '33522e742cc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('session', sa.Column('template_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_session_template_id_template',
        'session',
        'template',
        ['template_id'],
        ['id'],
    )

    # Backfill from existing session -> session_component -> question linkage.
    op.execute(
        """
        UPDATE session AS s
        SET template_id = src.template_id
        FROM (
            SELECT sc.session_id, MIN(q.template_id) AS template_id
            FROM session_component AS sc
            JOIN question AS q ON q.id = sc.question_id
            GROUP BY sc.session_id
        ) AS src
        WHERE s.id = src.session_id;
        """
    )


def downgrade():
    op.drop_constraint('fk_session_template_id_template', 'session', type_='foreignkey')
    op.drop_column('session', 'template_id')
