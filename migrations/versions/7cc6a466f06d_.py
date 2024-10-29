"""empty message

Revision ID: 7cc6a466f06d
Revises: 36d3e45d55fd
Create Date: 2024-10-26 10:35:56.419710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cc6a466f06d'
down_revision = '36d3e45d55fd'
branch_labels = None
depends_on = None


def upgrade():
    # Renombrar la tabla 'favoritos' a 'favorites' 
    op.rename_table('favoritos', 'favorites')


def downgrade():
    # En caso de que necesites revertir el cambio, renombrar de vuelta
    op.rename_table('favorites', 'favoritos')
