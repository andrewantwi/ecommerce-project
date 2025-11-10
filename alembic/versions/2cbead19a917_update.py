"""update

Revision ID: 2cbead19a917
Revises: 2164b742bc84
Create Date: 2025-11-10 14:03:02.111459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cbead19a917'
down_revision: Union[str, None] = '2164b742bc84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
