from pydantic import BaseModel
from src.models.user_notification import NotificationChannelType


class SendMessageSchema(BaseModel):
    task_id: str
    user_id: str
    notification_channel_type: NotificationChannelType
    notification_id: str
    template_id: str
    subject: str
    text: str
