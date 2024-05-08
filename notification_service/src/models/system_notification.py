from enum import IntEnum
from uuid import UUID

from sqlalchemy.orm import Mapped
from src.models.base import Base, NotificationStatus


class ContentType(IntEnum):
    user_registered = 0
    user_activated = 1
    user_deactivated = 2
    film_published = 3
    bookmark_expired = 4


class SystemNotificationTask(Base):
    __tablename__ = "system_notifications"
    content_type: Mapped[ContentType]
    content_id: Mapped[UUID]

    def __init__(
        self,
        content_type: ContentType,
        content_id: UUID,
        status: NotificationStatus,
    ):
        super().__init__(status=status)
        self.content_type = content_type  # type: ignore
        self.content_id = content_id  # type: ignore
