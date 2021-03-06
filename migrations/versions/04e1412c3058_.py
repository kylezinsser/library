"""empty message

Revision ID: 04e1412c3058
Revises: 4fc5e9929e1a
Create Date: 2021-05-26 00:57:15.940250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e1412c3058'
down_revision = '4fc5e9929e1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actor', schema=None) as batch_op:
        batch_op.drop_constraint('uq_actor_first_name', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_actor_first_name'), ['first_name', 'last_name'])

    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.drop_constraint('uq_author_first_name', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_author_first_name'), ['first_name', 'last_name'])

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('uq_book_universe_id', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_book_title'), ['title'])

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint('uq_character_series_id', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_character_series_id'), ['series_id', 'first_name', 'last_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_character_series_id'), type_='unique')
        batch_op.create_unique_constraint('uq_character_series_id', ['series_id', 'first_name', 'last_name', 'suffix'])

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_book_title'), type_='unique')
        batch_op.create_unique_constraint('uq_book_universe_id', ['universe_id', 'series_id', 'title'])

    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_author_first_name'), type_='unique')
        batch_op.create_unique_constraint('uq_author_first_name', ['first_name', 'middle_name', 'last_name', 'suffix'])

    with op.batch_alter_table('actor', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_actor_first_name'), type_='unique')
        batch_op.create_unique_constraint('uq_actor_first_name', ['first_name', 'middle_name', 'last_name', 'suffix'])

    # ### end Alembic commands ###
