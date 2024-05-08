from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from src.models.user_notification import (
    NotificationChannelType,
    NotificationStatus,
    UserNotificationTask,
)
from src.repositories.user_notification_task import UserNotificationTaskRepositoryABC


class UserNotificationServiceABC(ABC):
    @abstractmethod
    async def get_all_notifications(
        self, *, skip: int = 0, limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        ...

    @abstractmethod
    async def get_all_channel_notifications(
        self,
        *,
        channel_type: NotificationChannelType,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        ...

    @abstractmethod
    async def search_notifications_by_id(
        self,
        *,
        user_id: UUID,
        filter_by: NotificationChannelType | None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        ...


class UserNotificationService(UserNotificationServiceABC):
    def __init__(self, repository: UserNotificationTaskRepositoryABC):
        self._repository = repository

    async def get_all_channel_notifications(
        self,
        *,
        channel_type: NotificationChannelType,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        return await self._repository.search_by_channel(
            channel_type=channel_type, status=status, skip=skip, limit=limit
        )

    async def get_all_notifications(
        self, *, skip: int = 0, limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def search_notifications_by_id(
        self,
        *,
        user_id: UUID,
        filter_by: NotificationChannelType | None,
        skip: int = 0,
        limit: int = 100
    ):
        return await self._repository.search_by_id(
            user_id=user_id, filter_by=filter_by, skip=skip, limit=limit
        )
