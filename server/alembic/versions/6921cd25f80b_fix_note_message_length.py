"""Fix note message length

Revision ID: 6921cd25f80b
Revises: 84d2906ce9d9
Create Date: 2021-07-07 02:12:55.292226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6921cd25f80b'
down_revision = '84d2906ce9d9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'note',
        'message',
        existing_type=sa.String(256),
        type_=sa.String(2048),
        existing_nullable=False
    )


def downgrade():
    op.alter_column(
        'note',
        'message',
        existing_type=sa.String(2048),
        type_=sa.String(256),
        existing_nullable=False
    )
