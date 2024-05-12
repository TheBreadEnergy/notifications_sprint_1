from abc import ABC, abstractmethod
from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateModelType = TypeVar("CreateModelType", bound=BaseModel)


class RepositoryABC(ABC):
    @abstractmethod
    def gets(self, *args, **kwargs):
        ...

    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def insert(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...


class PostgresRepository(RepositoryABC, Generic[ModelType, CreateModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self._model = model
        self._session = session

    async def gets(self, *, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        statement = select(self._model)
        statement = statement.offset(skip).limit(limit)
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def get(self, *, entity_id: UUID) -> ModelType | None:
        statement = select(self._model).where(self._model.id == entity_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def insert(self, data: CreateModelType) -> ModelType:
        database_obj = self._model(**data.model_dump())
        self._session.add(database_obj)
        await self._session.commit()
        return database_obj

    async def delete(self, *, entity_id: UUID):
        statement = delete(self._model).where(self._model.id == entity_id)
        await self._session.execute(statement)
