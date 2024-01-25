from functools import cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio.client import Redis
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.person import Person
from src.services.cache import RedisCache
from src.services.persons import (
    CachedPersonRepository,
    PersonRepositoryES,
    PersonService,
    PersonServiceABC,
)


@add_factory_to_mapper(PersonServiceABC)
@cache
def create_person_service(
    session: AsyncElasticsearch = Depends(get_elastic),
    redis_client: Redis = Depends(get_redis),
) -> PersonService:
    repository = PersonRepositoryES(es=session, index="persons", model=Person)
    cache_storage = RedisCache(redis=redis_client, model=Person)
    return PersonService(
        repository=CachedPersonRepository(
            repository=repository, cache=cache_storage, model=Person
        )
    )
