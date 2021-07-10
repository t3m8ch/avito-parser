"""Change tables

Revision ID: e7f2692f0f50
Revises: 80ecf09c85c4
Create Date: 2021-07-05 12:57:56.738363

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e7f2692f0f50'
down_revision = '80ecf09c85c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'subscription',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chat_id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chat_id', 'url')
    )
    op.create_table(
        'ad',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('price', sa.Numeric(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ad')
    op.drop_table('subscription')
    # ### end Alembic commands ###
