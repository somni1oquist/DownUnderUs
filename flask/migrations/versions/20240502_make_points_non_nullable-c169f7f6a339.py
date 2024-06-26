"""Make points non-nullable

Revision ID: c169f7f6a339
Revises: d11c6851bf11
Create Date: 2024-05-02 11:32:06.675266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c169f7f6a339'
down_revision = 'd11c6851bf11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('points',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('points',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
