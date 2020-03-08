"""Journal additional info

Revision ID: 23125d9a026b
Revises: 6e9b74cfe4c0
Create Date: 2021-07-06 13:20:39.769153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23125d9a026b'
down_revision = '6e9b74cfe4c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'journal_note_additional',

        sa.Column(
            'id',
            sa.Integer,
            sa.ForeignKey('note.id'),
            primary_key=True
        ),

        sa.Column('mood', sa.Integer, nullable=True),
        sa.Column('sleep', sa.Integer, nullable=True),
        sa.Column('stress', sa.Integer, nullable=True),
        sa.Column('food', sa.Integer, nullable=True)
    )


def downgrade():
    op.drop_table('journal_note_additional')
