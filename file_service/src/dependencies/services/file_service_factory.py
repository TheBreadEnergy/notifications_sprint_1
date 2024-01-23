from functools import cache

from aiohttp import ClientSession
from fastapi import Depends
from miniopy_async import Minio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.file import File
from src.services.base import CachedRepository
from src.services.cache import RedisCache
from src.services.file import (
    FileMetaService,
    FileMetaServiceABC,
    FileRepository,
    FileService,
    FileServiceABC,
)
from src.storage.base import MinioStorage
from src.storage.minio import get_minio
from src.storage.session_client import get_client_session


@add_factory_to_mapper(FileServiceABC)
@cache
def create_file_service(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
    minio: Minio = Depends(get_minio),
    client_session: ClientSession = Depends(get_client_session),
) -> FileServiceABC:
    storage = MinioStorage(minio_client=minio, session_client=client_session)
    repository = FileRepository(db=session, model=File)
    redis_cache = RedisCache(redis=redis, model=File)
    cached_repository = CachedRepository(
        repository=repository, cache=redis_cache, model=File
    )
    return FileService(repository=cached_repository, storage=storage)


@add_factory_to_mapper(FileMetaServiceABC)
@cache
def create_file_meta_service(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> FileMetaServiceABC:
    repository = FileRepository(db=session, model=File)
    redis_cache = RedisCache(redis=redis, model=File)
    cached_repository = CachedRepository(
        repository=repository, cache=redis_cache, model=File
    )
    return FileMetaService(repository=cached_repository)
