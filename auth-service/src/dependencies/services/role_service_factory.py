from functools import cache

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.role import Role
from src.services.base import CachedRepository, SqlAlchemyUnitOfWork
from src.services.cache import RedisCacheService
from src.services.role import RoleServiceABC, RoleRepository, RoleService


@add_factory_to_mapper(RoleServiceABC)
@cache
def create_role_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> RoleServiceABC:
    role_repository = RoleRepository(session=session)
    cache_service = RedisCacheService(client=redis, model=Role)
    cached_repository = CachedRepository(
        repository=role_repository, cache_service=cache_service, model=Role
    )
    unit_of_work = SqlAlchemyUnitOfWork(session=session)
    return RoleService(repository=cached_repository, uow=unit_of_work)
