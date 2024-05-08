from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_notification import (
    NotificationChannelType,
    NotificationStatus,
    UserNotificationTask,
)
from src.repositories.base import PostgresRepository, RepositoryABC


class UserNotificationTaskRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def search_by_channel(
        self,
        *,
        channel_type: NotificationChannelType,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        ...

    @abstractmethod
    async def search_by_id(
        self,
        *,
        user_id: UUID,
        filter_by: NotificationChannelType | None = None,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        ...


class UserNotificationTaskRepository(
    PostgresRepository[UserNotificationTask], UserNotificationTaskRepositoryABC
):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=UserNotificationTask)

    async def search_by_channel(
        self,
        *,
        channel_type: NotificationChannelType,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        statement = select(UserNotificationTask)
        if status:
            statement = statement.where(
                and_(
                    UserNotificationTask.notification_channel_type == channel_type,
                    UserNotificationTask.status == status,
                )
            )
        else:
            statement = statement.where(
                UserNotificationTask.notification_channel_type == channel_type
            )

        statement = statement.offset(skip).limit(limit)
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def search_by_id(
        self,
        *,
        user_id: UUID,
        filter_by: NotificationChannelType | None = None,
        status: NotificationStatus | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        statement = select(UserNotificationTask)
        if filter_by:
            statement = statement.where(
                and_(
                    UserNotificationTask.user_id == user_id,
                    UserNotificationTask.notification_channel_type == filter_by,
                    UserNotificationTask.status == status,
                )
            )
        else:
            statement = statement.where(UserNotificationTask.user_id == user_id)
        statement = statement.offset(skip).limit(limit)
        results = await self._session.execute(statement)
        return results.scalars().all()
