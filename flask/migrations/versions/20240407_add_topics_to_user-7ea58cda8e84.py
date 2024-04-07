"""Add topics to user

Revision ID: 7ea58cda8e84
Revises: 95f9f11a87fb
Create Date: 2024-04-07 13:26:30.364769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ea58cda8e84'
down_revision = '95f9f11a87fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('topics', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('topics')

    # ### end Alembic commands ###
