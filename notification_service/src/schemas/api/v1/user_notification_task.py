import datetime
from uuid import UUID

from pydantic import BaseModel
from src.models.base import NotificationStatus
from src.models.user_notification import NotificationChannelType, NotificationType


class UserNotificationTaskSchema(BaseModel):
    id: UUID
    user_id: UUID
    notification_type: NotificationType
    notification_channel_type: NotificationChannelType
    notification_id: UUID
    template_id: UUID
    subject: str
    text: str
    status: NotificationStatus
    last_notification_send: datetime.datetime | None
