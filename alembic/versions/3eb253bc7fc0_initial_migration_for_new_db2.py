"""Initial migration for new DB2

Revision ID: 3eb253bc7fc0
Revises: ec2eddd9f63f
Create Date: 2025-02-19 16:45:43.157731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eb253bc7fc0'
down_revision: Union[str, None] = 'ec2eddd9f63f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'tax_rate')
    op.drop_column('products', 'stock_quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('stock_quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('products', sa.Column('tax_rate', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
