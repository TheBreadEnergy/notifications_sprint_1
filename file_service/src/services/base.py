from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.database import Base
from src.services.cache import Cache

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class Repository(ABC):
    @abstractmethod
    def gets(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_by_name(self, *args, **kwargs):
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


class PostgresRepository(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self._model = model
        self._db = db

    async def gets(self, *, skip=0, limit=100) -> list[ModelType]:
        statement = select(self._model).order_by().offset(skip).limit(limit)
        results = await self._db.execute(statement=statement)
        return results.scalars().all()

    async def get(self, *, entity_id: int) -> ModelType:
        statement = select(self._model).where(self._model.id == entity_id)
        results = await self._db.execute(statement)
        return results.scalar_one_or_none()

    async def get_by_name(self, *, short_name: str) -> ModelType:
        statement = select(self._model).where(self._model.short_name == short_name)
        results = await self._db.execute(statement)
        return results.scalar_one_or_none()

    async def insert(self, *, obj: CreateSchemaType) -> ModelType:
        raw_obj = jsonable_encoder(obj)
        database_obj = self._model(**raw_obj)
        self._db.add(database_obj)
        await self._db.commit()
        return database_obj

    async def delete(self, *, entity_id: Any) -> None:
        statement = delete(self._model).where(self._model.id == entity_id)
        await self._db.execute(statement)


class CachedRepository(
    PostgresRepository[ModelType, CreateSchemaType],
    Generic[ModelType, CreateSchemaType],
):
    def __init__(
        self,
        repository: PostgresRepository[ModelType, CreateSchemaType],
        cache: Cache,
        model: Type[ModelType],
    ):
        self._repository = repository
        self._cache = cache
        self._model = model

    async def gets(self, *, skip=0, limit=100) -> list[ModelType]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def get(self, *, entity_id: Any) -> ModelType | None:
        key = f"{self._model.__name__}_{entity_id}"
        entity = await self._cache.get(key=key)

        if not entity:
            entity = await self._repository.get(entity_id=entity_id)
            if entity:
                await self._cache.put(key=key, value=entity)
        return entity

    async def get_by_name(self, *, short_name: str) -> ModelType | None:
        key = f"{self._model.__name__}_name_{short_name}"
        entity = await self._cache.get(key=key)
        if not entity:
            entity = await self._repository.get_by_name(short_name=short_name)
            if entity:
                await self._cache.put(key=key, value=entity)
        return entity

    async def insert(self, *, obj: CreateSchemaType):
        return await self._repository.insert(obj=obj)

    async def delete(self, *, entity_id: Any):
        await self._repository.delete(entity_id=entity_id)
