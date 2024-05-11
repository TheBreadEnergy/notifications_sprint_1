import json
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from redis.asyncio import Redis
from src.models.base import CacheableABC

ModelType = TypeVar("ModelType", bound=CacheableABC)


class CacheABC(ABC, Generic[ModelType]):
    @abstractmethod
    async def get(self, *args, **kwargs):
        ...

    @abstractmethod
    async def set(self, *args, **kwargs):
        ...

    @abstractmethod
    async def delete(self, *args, **kwargs):
        ...


class RedisCache(CacheABC, Generic[ModelType]):
    def __init__(self, redis: Redis, model: Type[ModelType]):
        self._redis = redis
        self._model = model

    async def get(self, *, key: str) -> ModelType | None:
        value = await self._redis.get(key)
        if not value:
            return None
        return self._model(**json.loads(value))

    async def set(self, *, key: str, value: ModelType) -> ModelType:
        return await self._redis.set(
            key, json.dumps(value.serialize_object(), default=str)
        )

    async def delete(self, *, key: str) -> None:
        return await self._redis.delete(key)
