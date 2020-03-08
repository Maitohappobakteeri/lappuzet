"""add note category

Revision ID: 7b6e547c27e7
Revises: 89c3091cafc5
Create Date: 2021-05-13 20:32:08.546361

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7b6e547c27e7'
down_revision = '89c3091cafc5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'note_category',

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column(
            "owner", sa.Integer, nullable=False
        ),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('deleted_at', sa.DateTime),
    )

    op.add_column(
        'note',
        sa.Column(
            'category',
            sa.Integer,
            sa.ForeignKey('note_category.id'),
        )
    )


def downgrade():
    op.drop_table('note_category')
    op.drop_column('note', 'category')
