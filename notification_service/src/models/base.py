import datetime
import uuid

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.models.user_notification import NotificationStatus


class Base(DeclarativeBase):
    id = mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4
    )
    status: Mapped[NotificationStatus]
    last_updated: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
    last_notification_send: Mapped[datetime.datetime]
