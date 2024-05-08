from abc import ABC, abstractmethod
from typing import Callable, Sequence
from uuid import UUID

from sqlalchemy import false, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.system_notification import ContentType, SystemNotification
from src.repositories.base import PostgresRepository, RepositoryABC


class SystemNotificationRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def search_by_type(
        self, *, content_type: ContentType, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotification]:
        ...

    @abstractmethod
    async def search_by_id(
        self, *, content_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotification]:
        ...


class SystemNotificationRepository(
    PostgresRepository[SystemNotification], SystemNotificationRepositoryABC
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=SystemNotification)

    async def search_by_type(
        self, *, content_type: ContentType, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotification]:
        statement = self.build_statement(
            lambda: SystemNotification.content_type == content_type, skip, limit
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def search_by_id(
        self, *, content_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[SystemNotification]:
        statement = self.build_statement(
            lambda: SystemNotification.content_id == content_id, skip, limit
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    @staticmethod
    def build_statement(criterion: Callable[[], bool], offset: int, limit: int):
        return (
            select(SystemNotification)
            .where(or_(false(), criterion()))
            .offset(offset)
            .limit(limit)
        )
