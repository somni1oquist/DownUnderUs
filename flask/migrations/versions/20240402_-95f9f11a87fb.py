"""empty message

Revision ID: 95f9f11a87fb
Revises: 13504f96ae63
Create Date: 2024-04-02 10:08:08.515133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95f9f11a87fb'
down_revision = '13504f96ae63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('topic',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('topic',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###
