import datetime
from uuid import UUID

from pydantic import BaseModel
from src.models.base import NotificationStatus
from src.models.system_notification import ContentType


class SystemNotificationTaskSchema(BaseModel):
    id: UUID
    content_type: ContentType
    content_id: UUID
    status: NotificationStatus
    last_notification_send: datetime.datetime | None
