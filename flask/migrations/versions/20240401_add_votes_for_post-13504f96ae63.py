"""add votes for post

Revision ID: 13504f96ae63
Revises: 0b78faab8bcd
Create Date: 2024-04-01 17:06:57.019078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13504f96ae63'
down_revision = '0b78faab8bcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('votes', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('votes')

    # ### end Alembic commands ###
