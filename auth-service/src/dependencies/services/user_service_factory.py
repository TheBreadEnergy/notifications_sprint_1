from functools import cache

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.role import Role
from src.models.user import User
from src.services.base import SqlAlchemyUnitOfWork, CachedRepository
from src.services.cache import RedisCacheService
from src.services.role import UserRoleServiceABC, RoleRepository, UserRoleService
from src.services.user import UserServiceABC, UserRepository, UserService


@add_factory_to_mapper(UserServiceABC)
@cache
def create_user_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> UserServiceABC:
    base_repository = UserRepository(session=session)
    cache_service = RedisCacheService(client=redis, model=User)
    unit_of_work = SqlAlchemyUnitOfWork(session=session)
    cached_repository = CachedRepository(
        repository=base_repository, cache_service=cache_service, model=User
    )
    return UserService(repository=cached_repository, uow=unit_of_work)
