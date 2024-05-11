from functools import cache

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.cache.cache import RedisCache
from src.cache.redis import get_redis
from src.database.postgres import get_session
from src.dependencies.registrator import add_factory_to_mapper
from src.models.short_link import ShortLink
from src.repositories.links import CacheableLinksRepository, LinksRepository
from src.services.base import Md5ShortUrlGenerator
from src.services.links import LinksShortener, LinksShortenerABC


@add_factory_to_mapper(LinksShortenerABC)
@cache
def create_link_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> LinksShortener:
    cache_service = RedisCache(redis=redis, model=ShortLink)
    repository = LinksRepository(session=session)
    cached_repository = CacheableLinksRepository(
        repository=repository, cache=cache_service
    )
    algorithm = Md5ShortUrlGenerator()
    return LinksShortener(
        repository=cached_repository,
        algorithm=algorithm,
    )
