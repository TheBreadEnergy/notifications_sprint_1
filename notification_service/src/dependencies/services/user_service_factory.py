from functools import cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.dependencies.registrator import add_factory_to_mapper
from src.repositories.user_notification_task import UserNotificationTaskRepository
from src.services.user_notification import (
    UserNotificationService,
    UserNotificationServiceABC,
)


@add_factory_to_mapper(UserNotificationServiceABC)
@cache
def create_user_notification_service(
    session: AsyncSession = Depends(get_session),
) -> UserNotificationService:
    return UserNotificationService(
        repository=UserNotificationTaskRepository(session=session)
    )
