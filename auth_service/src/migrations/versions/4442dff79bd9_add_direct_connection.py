"""Add direct connection

Revision ID: 4442dff79bd9
Revises: 69f4972950b3
Create Date: 2024-02-17 11:07:15.112262

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4442dff79bd9"
down_revision: Union[str, None] = "69f4972950b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
