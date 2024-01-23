import logging
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar
from uuid import UUID

import backoff
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_scan
from src.core.config import BACKOFF_CONFIG
from src.services.cache import Cache

ModelType = TypeVar("ModelType")


class Repository(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def gets(self, *args, **kwargs):
        ...

    @abstractmethod
    def find(self, *args, **kwargs):
        ...


class RepositoryES(Repository, Generic[ModelType]):
    def __init__(
        self, index: str, es: AsyncElasticsearch, model: Type[ModelType]
    ) -> None:
        self._db = es
        self._index = index
        self._model = model

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def get(self, entity_id: UUID) -> ModelType | None:
        try:
            document = await self._db.get(index=self._index, id=str(entity_id))
        except NotFoundError:
            return None
        return self._model(**document["_source"])

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[ModelType]:
        documents = []
        offset_min = (page - 1) * size
        offset_max = page * size
        query = self.build_gets_query(sort=sort, data_filter=data_filter)
        async for document in async_scan(
            self._db, query=query, index=self._index, preserve_order=True
        ):
            documents.append(self._model(**document["_source"]))
        return documents[offset_min:offset_max]

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def find(self, *, title: str, page: int, size: int) -> list[ModelType]:
        documents = []
        offset_min = (page - 1) * size
        offset_max = page * size
        query = self.build_find_query(title=title)
        async for document in async_scan(
            self._db, query=query, index=self._index, preserve_order=True
        ):
            documents.append(self._model(**document["_source"]))
        return documents[offset_min:offset_max]

    @abstractmethod
    def build_gets_query(self, *, sort: str, data_filter: dict) -> dict:
        ...

    @abstractmethod
    def build_find_query(self, title: str) -> dict:
        ...


class CachedRepositoryES(RepositoryES[ModelType], Generic[ModelType]):
    def __init__(
        self, repository: RepositoryES[ModelType], cache: Cache, model: Type[ModelType]
    ):
        self._repository = repository
        self._cache = cache
        self._model = model

    async def get(self, entity_id: UUID) -> ModelType | None:
        key = f"{self._model.__name__}_{entity_id}"
        document = await self._cache.get(key=key)
        if document:
            logging.info(f"Cache hit. Document {entity_id} taken from cache.")
        if not document:
            logging.info(f"Cache miss. Document {entity_id} taken from database.")
            document = await self._repository.get(entity_id=entity_id)
            await self._cache.put(key=key, value=document)
            logging.info(f"Put document {entity_id} to cache.")
        return document

    async def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[ModelType]:
        return await self._repository.gets(
            sort=sort, data_filter=data_filter, page=page, size=size
        )

    async def find(self, *, title: str, page: int, size: int) -> list[ModelType]:
        return await self._repository.find(title=title, page=page, size=size)

    def build_gets_query(self, *, sort: str, data_filter: dict) -> dict:
        return self._repository.build_gets_query(sort=sort, data_filter=data_filter)

    def build_find_query(self, title: str) -> dict:
        return self._repository.build_find_query(title=title)
