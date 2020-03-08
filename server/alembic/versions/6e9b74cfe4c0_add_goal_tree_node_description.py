"""Add goal tree node description

Revision ID: 6e9b74cfe4c0
Revises: fa4da1996384
Create Date: 2021-05-15 15:20:32.503397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e9b74cfe4c0'
down_revision = 'fa4da1996384'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'goal_tree_node',
        sa.Column('description', sa.String(512))
    )


def downgrade():
    op.drop_column('goal_tree_node', 'description')
