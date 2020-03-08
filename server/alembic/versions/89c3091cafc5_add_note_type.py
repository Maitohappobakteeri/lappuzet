"""add note type

Revision ID: 89c3091cafc5
Revises: 38383f7f9ba5
Create Date: 2020-03-29 04:40:00.512060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c3091cafc5'
down_revision = '893da05741f3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'note',
        sa.Column('type', sa.CHAR(32), nullable=False, server_default="note")
    )
    op.alter_column(
        'note',
        'type', server_default=None
    )


def downgrade():
    op.drop_column('note', 'type')
