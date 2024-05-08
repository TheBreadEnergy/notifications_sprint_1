from abc import ABC, abstractmethod
from typing import Callable, Sequence
from uuid import UUID

from sqlalchemy import false, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.system_notification import ContentType, SystemNotificationTask
from src.repositories.base import PostgresRepository, RepositoryABC


class SystemNotificationRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def search_by_type(
        self, *, content_type: ContentType, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...

    @abstractmethod
    async def search_by_id(
        self, *, content_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        ...


class SystemNotificationRepository(
    PostgresRepository[SystemNotificationTask], SystemNotificationRepositoryABC
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=SystemNotificationTask)

    async def search_by_type(
        self, *, content_type: ContentType, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        statement = self.build_statement(
            lambda: SystemNotificationTask.content_type == content_type, skip, limit
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def search_by_id(
        self, *, content_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotificationTask]:
        statement = self.build_statement(
            lambda: SystemNotificationTask.content_id == content_id, skip, limit
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    @staticmethod
    def build_statement(criterion: Callable[[], bool], offset: int, limit: int):
        return (
            select(SystemNotificationTask)
            .where(or_(false(), criterion()))
            .offset(offset)
            .limit(limit)
        )
