from enum import IntEnum
from typing import Mapping
from uuid import UUID

from src.models.base import Base


class ContentType(IntEnum):
    user_registered = 0
    user_activated = 1
    user_deactivated = 2
    film_published = 3
    bookmark_expired = 4


class SystemNotificationTask(Base):
    __tablename__ = "system_notifications"
    content_type: Mapping[ContentType]
    content_id: Mapping[UUID]

    def __init__(self, content_type: ContentType, content_id: UUID):
        super().__init__()
        self.content_type = content_type  # type: ignore
        self.content_id = content_id  # type: ignore
