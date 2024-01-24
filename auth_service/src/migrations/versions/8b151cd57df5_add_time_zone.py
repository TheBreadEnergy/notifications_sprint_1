"""ADD TIME ZONE

Revision ID: 8b151cd57df5
Revises: cce28a54a5cb
Create Date: 2024-01-24 13:51:34.128495

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b151cd57df5"
down_revision: Union[str, None] = "cce28a54a5cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
