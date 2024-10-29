"""empty message

Revision ID: 390319d12874
Revises: fbc881a0449c
Create Date: 2024-10-28 23:06:30.354918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '390319d12874'
down_revision = 'fbc881a0449c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('person_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('unique_favorite', type_='unique')
        batch_op.create_unique_constraint('unique_favorite_person', ['user_id', 'person_id'])
        batch_op.create_unique_constraint('unique_favorite_planet', ['user_id', 'planet_id'])
        batch_op.create_foreign_key(None, 'people', ['person_id'], ['id'])
        batch_op.create_foreign_key(None, 'planets', ['planet_id'], ['id'])
        batch_op.drop_column('fav_id')
        batch_op.drop_column('fav_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fav_type', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('fav_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint('unique_favorite_planet', type_='unique')
        batch_op.drop_constraint('unique_favorite_person', type_='unique')
        batch_op.create_unique_constraint('unique_favorite', ['user_id', 'fav_type', 'fav_id'])
        batch_op.drop_column('person_id')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###