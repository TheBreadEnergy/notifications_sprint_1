from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_notification import NotificationChannelType, UserNotificationTask
from src.repositories.base import PostgresRepository, RepositoryABC


class UserNotificationRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def search_by_id(
        self,
        *,
        user_id: UUID,
        filter_by: NotificationChannelType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        ...


class UserNotificationRepository(
    PostgresRepository[UserNotificationTask], UserNotificationRepositoryABC
):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=UserNotificationTask)

    async def search_by_id(
        self,
        *,
        user_id: UUID,
        filter_by: NotificationChannelType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[UserNotificationTask]:
        statement = select(UserNotificationTask)
        if filter_by:
            statement = statement.where(
                and_(
                    UserNotificationTask.user_id == user_id,
                    UserNotificationTask.notification_channel_type == filter_by,
                )
            )
        else:
            statement = statement.where(UserNotificationTask.user_id == user_id)
        statement = statement.offset(skip).limit(limit)
        results = await self._session.execute(statement)
        return results.scalars().all()
