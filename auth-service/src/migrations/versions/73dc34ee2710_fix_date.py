"""fix date

Revision ID: 73dc34ee2710
Revises: c3026f733516
Create Date: 2024-01-23 14:51:32.562202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73dc34ee2710'
down_revision: Union[str, None] = 'c3026f733516'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
