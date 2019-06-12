"""added image to products

Revision ID: 6b226fac7e79
Revises: 6d505177c151
Create Date: 2019-06-12 17:11:46.426278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b226fac7e79'
down_revision = '6d505177c151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('image', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'image')
    # ### end Alembic commands ###