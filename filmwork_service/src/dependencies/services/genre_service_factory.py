from functools import cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio.client import Redis
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.genre import Genre
from src.services.cache import RedisCache
from src.services.genres import (
    CachedGenreRepository,
    GenreRepository,
    GenreService,
    GenreServiceABC,
)


@add_factory_to_mapper(GenreServiceABC)
@cache
def create_genre_service(
    session: AsyncElasticsearch = Depends(get_elastic),
    redis_client: Redis = Depends(get_redis),
) -> GenreService:
    repository = GenreRepository(es=session, index="genres", model=Genre)
    cache_storage = RedisCache(redis=redis_client, model=Genre)
    return GenreService(
        repository=CachedGenreRepository(
            repository=repository, cache=cache_storage, model=Genre
        )
    )
