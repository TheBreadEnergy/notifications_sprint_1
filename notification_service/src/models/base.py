import datetime
import uuid
from enum import IntEnum

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class NotificationStatus(IntEnum):
    pending = 0
    started = 1
    in_progress = 2
    completed = 3
    cancelled = 4
    sceduled = 5


class Base(DeclarativeBase):
    id = mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4()
    )
    status: Mapped[NotificationStatus]
    last_updated: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
    last_notification_send: Mapped[datetime.datetime]
