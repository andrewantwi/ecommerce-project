"""Initial migration for new DB13

Revision ID: 9c4138172206
Revises: 7fa959f4e97c
Create Date: 2025-02-21 13:15:11.481397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4138172206'
down_revision: Union[str, None] = '7fa959f4e97c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_items', sa.Column('price', sa.Float(), nullable=False))
    op.drop_column('cart_items', 'unit_price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_items', sa.Column('unit_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('cart_items', 'price')
    # ### end Alembic commands ###
