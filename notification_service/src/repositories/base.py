from abc import ABC, abstractmethod
from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class RepositoryABC(ABC):
    @abstractmethod
    def gets(self, *args, **kwargs):
        ...

    @abstractmethod
    def get(self, *args, **kwargs):
        ...


class PostgresRepository(RepositoryABC, Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self._model = model
        self._session = session

    async def gets(self, *, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        statement = select(self._model).offset(skip).limit(limit)
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def get(self, *, entity_id: UUID) -> ModelType:
        statement = select(self._model).where(self._model.id == entity_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
