import datetime
import uuid
from uuid import UUID

import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.config import settings
from src.models.base import Base


def create_default_expires():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=settings.long_live_seconds
    )


class ShortLink(Base):
    __tablename__ = "short_links"
    id: Mapped[UUID] = mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    short_link: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    original_link: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        default=create_default_expires,
    )

    class Config:
        orm_mode = True

    def __init__(
        self,
        short_link: str,
        original_link: str,
        expires_at: datetime.datetime = create_default_expires(),
        id: UUID = None,
    ):
        if id:
            self.id = id  # noqa

        self.short_link = short_link  # noqa
        self.original_link = original_link  # noqa
        self.expires_at = expires_at  # noqa

    def serialize_object(self, *args, **kwargs):
        return {
            "id": self.id,
            "short_link": str(self.short_link),
            "original_link": str(self.original_link),
            "expires_at": self.expires_at,
        }
