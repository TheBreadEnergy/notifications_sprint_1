from functools import cache

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.user import User
from src.services.auth import AuthService, AuthServiceABC
from src.services.base import CachedRepository
from src.services.cache import RedisCacheService, TokenStorageABC
from src.services.user import UserRepository


@add_factory_to_mapper(AuthServiceABC)
@cache
def create_auth_service(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
    auth_jwt: AuthJWT = Depends(),
    token_storage: TokenStorageABC = Depends(),
) -> AuthServiceABC:
    user_repository = UserRepository(session=session)
    cache_service = RedisCacheService(client=redis, model=User)
    cached_user_repository = CachedRepository(
        repository=user_repository, cache_service=cache_service, model=User
    )
    return AuthService(
        auth_jwt_service=auth_jwt,
        token_storage=token_storage,
        user_repository=cached_user_repository,
    )
