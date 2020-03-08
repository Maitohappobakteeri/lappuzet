"""Increase note message length

Revision ID: 84d2906ce9d9
Revises: 23125d9a026b
Create Date: 2021-07-06 13:38:37.683584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84d2906ce9d9'
down_revision = '23125d9a026b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'note',
        'message',
        existing_type=sa.String(256),
        type=sa.String(2048)
    )


def downgrade():
    op.alter_column(
        'note',
        'message',
        existing_type=sa.String(2048),
        type=sa.String(256)
    )
