from functools import cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio.client import Redis
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.film import Film
from src.services.cache import RedisCache
from src.services.film import (
    CachedFilmRepository,
    FilmRepository,
    FilmService,
    FilmServiceABC,
)


@add_factory_to_mapper(FilmServiceABC)
@cache
def create_film_service(
    session: AsyncElasticsearch = Depends(get_elastic),
    redis_client: Redis = Depends(get_redis),
) -> FilmService:
    repository = FilmRepository(es=session, index="movies", model=Film)
    cache_storage = RedisCache(redis=redis_client, model=Film)
    return FilmService(
        repository=CachedFilmRepository(
            repository=repository, cache=cache_storage, model=Film
        )
    )
