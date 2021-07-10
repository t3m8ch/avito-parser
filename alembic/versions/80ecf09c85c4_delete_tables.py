"""Delete tables

Revision ID: 80ecf09c85c4
Revises: 431f6642b14c
Create Date: 2021-07-05 12:56:54.439729

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '80ecf09c85c4'
down_revision = '431f6642b14c'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('subscription')
    op.drop_table('ad')


def downgrade():
    op.create_table(
        'ad',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('price', sa.Numeric(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url')
    )
    op.create_table(
        'subscription',
        sa.Column('chat_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('chat_id'),
        sa.UniqueConstraint('url')
    )
