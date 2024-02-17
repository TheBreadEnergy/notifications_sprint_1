"""Add direct connection

Revision ID: 69f4972950b3
Revises: bbc417337833
Create Date: 2024-02-17 10:06:15.549513

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "69f4972950b3"
down_revision: Union[str, None] = "bbc417337833"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
