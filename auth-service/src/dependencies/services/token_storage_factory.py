from functools import cache

from fastapi import Depends
from redis.asyncio import Redis

from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.services.cache import TokenStorageABC, RedisTokenStorage


@add_factory_to_mapper(TokenStorageABC)
@cache
def create_token_storage(redis_client: Redis = Depends(get_redis)) -> TokenStorageABC:
    return RedisTokenStorage(client=redis_client)
