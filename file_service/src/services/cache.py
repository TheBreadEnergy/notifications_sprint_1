import json
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from redis.asyncio import Redis

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

    async def get(self, *, key: str) -> ModelType | None:
        document = await self._redis.get(key)
        if not document:
            return None
        return self._model(**json.loads(document))

    async def put(self, *, key: str, value: ModelType):
        document = value.to_dict()
        await self._redis.set(key, json.dumps(document))
