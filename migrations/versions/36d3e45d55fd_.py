"""empty message

Revision ID: 36d3e45d55fd
Revises: a5cffa318ac2
Create Date: 2024-10-26 09:57:07.314946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36d3e45d55fd'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('birth_year', sa.String(), nullable=False),
    sa.Column('eye_color', sa.String(), nullable=False),
    sa.Column('films', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('hair_color', sa.String(), nullable=False),
    sa.Column('height', sa.String(), nullable=False),
    sa.Column('homeworld', sa.String(), nullable=False),
    sa.Column('mass', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('skin_color', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('edited', sa.DateTime(), nullable=False),
    sa.Column('species', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('starships', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('vehicles', postgresql.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('climate', sa.String(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.Column('gravity', sa.String(), nullable=False),
    sa.Column('orbital_period', sa.Integer(), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('residents', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('rotation_period', sa.Integer(), nullable=False),
    sa.Column('surface_water', sa.Integer(), nullable=False),
    sa.Column('terrain', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('favoritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fav_type', sa.String(length=50), nullable=False),
    sa.Column('fav_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'fav_type', 'fav_id', name='unique_favorite')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=30), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    op.drop_table('favoritos')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###
