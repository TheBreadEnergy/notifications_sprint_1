from uuid import UUID

from pydantic import BaseModel
from src.models.user_notification import NotificationChannelType


class SendMessageSchema(BaseModel):
    task_id: UUID
    user_id: UUID
    notification_channel_type: NotificationChannelType
    notification_id: UUID
    template_id: UUID
    subject: str
    text: str
