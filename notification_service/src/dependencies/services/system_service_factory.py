from functools import cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.dependencies.registrator import add_factory_to_mapper
from src.repositories.system_notification_task import SystemNotificationTaskRepository
from src.services.system_notification import (
    SystemNotificationService,
    SystemNotificationServiceABC,
)


@add_factory_to_mapper(SystemNotificationServiceABC)
@cache
def create_system_notification_service(
    session: AsyncSession = Depends(get_session),
) -> SystemNotificationService:
    return SystemNotificationService(
        repository=SystemNotificationTaskRepository(session)
    )
