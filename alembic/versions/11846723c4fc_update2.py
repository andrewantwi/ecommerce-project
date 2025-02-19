"""update2

Revision ID: 11846723c4fc
Revises: aa67c233af48
Create Date: 2025-01-08 11:47:35.422218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '11846723c4fc'
down_revision: Union[str, None] = 'aa67c233af48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('appointment', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('appointment', 'condition',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
    op.drop_column('appointment', 'visit_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('visit_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.alter_column('appointment', 'condition',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.drop_column('appointment', 'updated_at')
    op.drop_column('appointment', 'created_at')
    # ### end Alembic commands ###
