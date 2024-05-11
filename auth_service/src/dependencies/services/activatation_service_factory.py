from functools import cache

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.db.redis import get_redis
from src.dependencies.registrator import add_factory_to_mapper
from src.models.user import User
from src.services.activation import ActivationService, ActivationServiceABC
from src.services.base import SqlAlchemyUnitOfWork
from src.services.cache import RedisCacheService
from src.services.event_handler import EventHandlerABC
from src.services.user import CachedUserRepository, UserRepository


@add_factory_to_mapper(ActivationServiceABC)
@cache
def create_activation_service(
    event_handler: EventHandlerABC = Depends(),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> ActivationService:
    base_repository = UserRepository(session=session)
    cache_service = RedisCacheService(client=redis, model=User)
    unit_of_work = SqlAlchemyUnitOfWork(session=session)
    cached_repository = CachedUserRepository(
        repository=base_repository, cache_service=cache_service
    )
    return ActivationService(
        repository=cached_repository, uow=unit_of_work, event_handler=event_handler
    )
