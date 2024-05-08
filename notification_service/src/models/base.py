import uuid

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    id = mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4
    )
