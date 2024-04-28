"""create_table_title and add registered date for user table

Revision ID: 22e1e8989ca7
Revises: ae4ca56eef7f
Create Date: 2024-04-28 21:27:05.723893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22e1e8989ca7'
down_revision = 'ae4ca56eef7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('title',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('awarded_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('title', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_title_awarded_date'), ['awarded_date'], unique=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.String(length=200), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('points', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('registered_date', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_registered_date'), ['registered_date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_registered_date'))
        batch_op.drop_column('registered_date')
        batch_op.drop_column('points')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('tags')

    with op.batch_alter_table('title', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_title_awarded_date'))

    op.drop_table('title')
    # ### end Alembic commands ###
