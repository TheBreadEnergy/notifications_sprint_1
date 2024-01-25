from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import Base
from src.services.cache import CacheServiceABC

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class UnitOfWork(ABC):
    @abstractmethod
    def commit(self, *args, **kwargs):
        ...


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self, *args, **kwargs) -> None:
        return await self._session.commit()


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


class PostgresRepository(RepositoryABC, Generic[ModelType, CreateSchemaType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self._model = model
        self._session = session

    async def gets(self, *, skip=0, limit=100) -> list[ModelType]:
        statement = select(self._model).order_by().offset(skip).limit(limit)
        results = await self._session.execute(statement=statement)
        return results.scalars().all()

    async def get(self, *, entity_id: int) -> ModelType:
        statement = select(self._model).where(self._model.id == entity_id)
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()

    async def insert(self, body: CreateSchemaType) -> ModelType:
        raw_obj = jsonable_encoder(body)
        database_obj = self._model(**raw_obj)
        self._session.add(database_obj)
        return database_obj

    async def delete(self, *, entity_id: Any):
        statement = delete(self._model).where(self._model.id == entity_id)
        await self._session.execute(statement)


class CachedRepository(
    PostgresRepository[ModelType, CreateSchemaType],
    Generic[ModelType, CreateSchemaType],
):
    def __init__(
        self,
        repository: PostgresRepository[ModelType, CreateSchemaType],
        cache_service: CacheServiceABC,
        model: Type[ModelType],
    ):
        self._model = model
        self._repository = repository
        self._cache = cache_service

    async def gets(self, *, skip=0, limit=100) -> list[ModelType]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def get(self, *, entity_id: int) -> ModelType:
        key = f"{self._model.__name__}_{entity_id}"
        entity = await self._cache.get(key=key)
        if not entity:
            entity = await self._repository.get(entity_id=entity_id)
        return entity

    async def insert(self, *, body: CreateSchemaType) -> ModelType:
        return await self._repository.insert(body=body)

    async def delete(self, *, entity_id: Any):
        await self._repository.delete(entity_id=entity_id)
