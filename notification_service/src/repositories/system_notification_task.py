from abc import ABC, abstractmethod
from typing import Callable, Sequence
from uuid import UUID

from sqlalchemy import ColumnElement, and_, select, true
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.system_notification import ContentType, SystemNotificationTask
from src.models.user_notification import NotificationType
from src.repositories.base import PostgresRepository, RepositoryABC


class SystemNotificationTaskRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def search_by_type(
        self,
        *,
        content_type: ContentType,
        status: NotificationType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...

    @abstractmethod
    async def search_by_id(
        self,
        *,
        content_id: UUID,
        status: NotificationType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...


class SystemNotificationTaskRepository(
    PostgresRepository[SystemNotificationTask], SystemNotificationTaskRepositoryABC
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=SystemNotificationTask)

    async def search_by_type(
        self,
        *,
        content_type: ContentType,
        status: NotificationType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        statement = self.build_statement(
            lambda: and_(
                SystemNotificationTask.content_type == content_type,
                SystemNotificationTask.status == status if status else true(),
            ),
            skip,
            limit,
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def search_by_id(
        self,
        *,
        content_id: UUID,
        status: NotificationType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        statement = self.build_statement(
            lambda: and_(
                SystemNotificationTask.content_id == content_id,
                SystemNotificationTask.status == status if status else true(),
            ),
            offset=skip,
            limit=limit,
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    @staticmethod
    def build_statement(
        criterion: Callable[[], ColumnElement[bool]],
        offset: int,
        limit: int,
    ):
        return (
            select(SystemNotificationTask).where(criterion).offset(offset).limit(limit)
        )
