"""Add tag field

Revision ID: 686506bbd9e2
Revises: 8d4e5a45da75
Create Date: 2021-07-05 15:50:19.626457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '686506bbd9e2'
down_revision = '8d4e5a45da75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscription', sa.Column('tag', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscription', 'tag')
    # ### end Alembic commands ###
