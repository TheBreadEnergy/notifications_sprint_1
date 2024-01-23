from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

import backoff
from redis.asyncio.client import Redis
from src.core.config import BACKOFF_CONFIG

ModelType = TypeVar("ModelType")


class Cache(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def put(self, *args, **kwargs):
        ...


class RedisCache(Cache, Generic[ModelType]):
    def __init__(self, redis: Redis, model: Type[ModelType]):
        self._redis = redis
        self._model = model

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def get(self, *, key: str) -> ModelType | None:
        document = await self._redis.get(key)
        if not document:
            return None
        return self._model.model_validate_json(document)

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def put(self, *, key: str, value: ModelType) -> None:
        await self._redis.set(key, value.json())
