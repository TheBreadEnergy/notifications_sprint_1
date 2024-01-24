from functools import cache

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.role import Role
from src.models.user import User
from src.services.base import CachedRepository, SqlAlchemyUnitOfWork
from src.services.cache import RedisCacheService
from src.services.role import RoleRepository, UserRoleService, UserRoleServiceABC
from src.services.user import UserRepository


@add_factory_to_mapper(UserRoleServiceABC)
@cache
def create_user_role_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> UserRoleServiceABC:
    user_repository = UserRepository(session=session)
    role_repository = RoleRepository(session=session)
    cache_service = RedisCacheService(client=redis, model=User)
    cached_user_repository = CachedRepository(
        repository=user_repository, cache_service=cache_service, model=User
    )
    cached_role_repository = CachedRepository(
        repository=role_repository, cache_service=cache_service, model=Role
    )
    unit_of_work = SqlAlchemyUnitOfWork(session=session)
    return UserRoleService(
        user_repository=cached_user_repository,
        role_repository=cached_role_repository,
        uow=unit_of_work,
    )
