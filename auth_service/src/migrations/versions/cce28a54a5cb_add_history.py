"""Add History

Revision ID: cce28a54a5cb
Revises: a029ec874b18
Create Date: 2024-01-24 13:40:31.555674

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cce28a54a5cb"
down_revision: Union[str, None] = "a029ec874b18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
