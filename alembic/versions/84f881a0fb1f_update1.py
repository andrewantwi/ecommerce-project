"""Update1

Revision ID: 84f881a0fb1f
Revises: dc19be493041
Create Date: 2025-02-24 09:03:45.911913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84f881a0fb1f'
down_revision: Union[str, None] = 'dc19be493041'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('shop_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'products', 'shops', ['shop_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'shop_id')
    # ### end Alembic commands ###
