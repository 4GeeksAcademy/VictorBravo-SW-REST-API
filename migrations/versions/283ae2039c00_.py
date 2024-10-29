"""empty message

Revision ID: 283ae2039c00
Revises: 7cc6a466f06d
Create Date: 2024-10-28 21:45:07.385236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283ae2039c00'
down_revision = '7cc6a466f06d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('edited', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('edited')
        batch_op.drop_column('created')

    # ### end Alembic commands ###
