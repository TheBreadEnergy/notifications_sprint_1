"""Initial

Revision ID: cb5260c1ddd7
Revises: 
Create Date: 2024-05-11 19:54:01.948862

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cb5260c1ddd7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "short_links",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("short_link", sa.String(length=255), nullable=False),
        sa.Column("original_link", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("original_link"),
        sa.UniqueConstraint("short_link"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("short_links")
    # ### end Alembic commands ###
