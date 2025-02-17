"""Remove uniqness of original link

Revision ID: 2d8c209265b4
Revises: cb5260c1ddd7
Create Date: 2024-05-11 20:00:35.312698

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2d8c209265b4"
down_revision: Union[str, None] = "cb5260c1ddd7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("short_links_original_link_key", "short_links", type_="unique")
    op.drop_constraint("short_links_short_link_key", "short_links", type_="unique")
    op.create_index(
        op.f("ix_short_links_short_link"), "short_links", ["short_link"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_short_links_short_link"), table_name="short_links")
    op.create_unique_constraint(
        "short_links_short_link_key", "short_links", ["short_link"]
    )
    op.create_unique_constraint(
        "short_links_original_link_key", "short_links", ["original_link"]
    )
    # ### end Alembic commands ###
