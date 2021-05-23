"""empty message

Revision ID: 7ddeb00088c3
Revises: f94b93d0a4bb
Create Date: 2021-05-23 00:14:35.161674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ddeb00088c3'
down_revision = 'f94b93d0a4bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('series_index', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('series_index')

    # ### end Alembic commands ###