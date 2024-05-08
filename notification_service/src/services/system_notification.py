from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from src.models.system_notification import ContentType, SystemNotificationTask
from src.models.user_notification import NotificationStatus
from src.repositories.system_notification_task import (
    SystemNotificationTaskRepositoryABC,
)


class SystemNotificationServiceABC(ABC):
    @abstractmethod
    async def get_all_notifications(
        self, *, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...

    @abstractmethod
    async def search_for_content_id(
        self,
        *,
        content_id: UUID,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...

    @abstractmethod
    async def search_by_content_type(
        self,
        *,
        content_type: ContentType,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...


class SystemNotificationService(SystemNotificationServiceABC):
    def __init__(self, repository: SystemNotificationTaskRepositoryABC):
        self._repository = repository

    async def get_all_notifications(
        self, *, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def search_for_content_id(
        self,
        *,
        content_id: UUID,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        return await self._repository.search_by_id(
            content_id=content_id, status=status, skip=skip, limit=limit
        )

    async def search_by_content_type(
        self,
        *,
        content_type: ContentType,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        await self._repository.search_by_type(
            content_type=content_type, status=status, skip=skip, limit=limit
        )
