import json
from abc import ABC, abstractmethod
from typing import Type, TypeVar

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

ModelType = TypeVar("ModelType")


class CacheServiceABC(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def put(self, *args, **kwargs):
        ...


class TokenStorageABC(ABC):
    @abstractmethod
    def store_token(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_token(self, *args, **kwargs):
        ...

    @abstractmethod
    def check_expiration(self, *args, **kwargs):
        ...


class RedisCacheService(CacheServiceABC):
    def __init__(self, client: Redis, model: Type[ModelType]):
        self._client = client
        self._model = model

    async def get(self, *, key: str) -> ModelType | None:
        document = await self._client.get(key)
        if not document:
            return None
        return self._model(**json.loads(document))

    async def put(self, *, key: str, value: ModelType):
        document = value.to_dict()
        await self._client.set(key, json.dumps(value))


class RedisTokenStorage(TokenStorageABC):
    def __init__(self, client: Redis):
        self._client = client

    async def get_token(self, *, key: str) -> bool:
        return await self._client.get(key)

    async def store_token(
        self, *, token: str, value: bool, expiration_time: int
    ) -> None:
        async def _store_token_inner(pipeline: Pipeline):
            await pipeline.setex(
                name=token,
                time=expiration_time,
                value=str(value),
            )

        await self._client.transaction(_store_token_inner)

    async def check_expiration(self, *, jti: str):
        return await self.get_token(key=jti) == "True"
