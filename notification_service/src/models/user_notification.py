import datetime
import uuid
from enum import IntEnum

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class NotificationChannelType(IntEnum):
    email = 0
    sms = 1
    push = 2


class NotificationType(IntEnum):
    fast_notification = 0
    delayed_notification = 1
    scheduled_notification = 2


class UserNotificationTask(Base):
    __tablename__ = "user_notifications"
    user_id: Mapped[uuid.UUID] = mapped_column(sqlalchemy.UUID(as_uuid=True))
    notification_type: Mapped[NotificationType]
    notification_channel_type: Mapped[NotificationChannelType]
    notification_id: Mapped[uuid.UUID]
    template_id: Mapped[uuid.UUID]
    subject: Mapped[str]
    text: Mapped[str]

    def __init__(
        self,
        user_id: uuid.UUID,
        notification_type: NotificationType,
        notification_channel_type: NotificationChannelType,
        notification_id: uuid.UUID,
        template_id: uuid.UUID,
        subject: str,
        text: str,
        execution_time: datetime.datetime | None = None,
    ):
        super().__init__()
        self.user_id = user_id  # type: ignore
        self.notification_type = notification_type  # type: ignore
        self.notification_channel_type = notification_channel_type  # type: ignore
        self.notification_id = notification_id  # type: ignore
        self.template_id = template_id  # type: ignore
        self.subject = subject  # type: ignore
        self.text = text  # type: ignore
        self.execution_time = execution_time  # type: ignore
