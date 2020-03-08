"""Add goal tree

Revision ID: fa4da1996384
Revises: 7b6e547c27e7
Create Date: 2021-05-14 05:19:24.338002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa4da1996384'
down_revision = '7b6e547c27e7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'goal_tree',

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column(
            "owner", sa.Integer, nullable=False
        ),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('deleted_at', sa.DateTime),
    )

    op.create_table(
        'goal_tree_node',

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(256), nullable=False),

        sa.Column(
            "tree", sa.Integer, sa.ForeignKey('goal_tree.id'), nullable=False
        ),
        sa.Column(
            "parent_node", sa.Integer, sa.ForeignKey('goal_tree_node.id')
        ),

        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('deleted_at', sa.DateTime),
        sa.Column('resolved_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('goal_tree')
    op.drop_table('goal_tree_node')
