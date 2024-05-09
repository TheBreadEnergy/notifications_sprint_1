from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from src.models.base import NotificationStatus
from src.models.user_notification import NotificationChannelType, UserNotificationTask
from src.schemas.api.v1.user_notification_task import UserNotificationTaskSchema
from src.services.user_notification import UserNotificationServiceABC

router = APIRouter()


@router.get(
    "/",
    description="Отображение всех пользовательских уведомлений "
    "отправленных менеджерами",
    response_model=list[UserNotificationTaskSchema],
    response_description="Список заданий на уведомление",
    tags=["Пользователи"],
)
async def get_user_notifications(
    user_notification_service: UserNotificationServiceABC = Depends(),
    status: NotificationStatus | None = None,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
) -> Sequence[UserNotificationTask]:
    return await user_notification_service.get_all_notifications(
        status=status, skip=skip, limit=limit
    )


@router.get(
    "/search/{user_id}",
    description="Выдача заданий об уведомлении для конкретного пользователя",
    response_model=list[UserNotificationTaskSchema],
    response_description="Список заданий на уведомление",
    tags=["Пользователи"],
)
async def get_user_notifications_for_specific_user(
    user_id: UUID,
    notification_service: UserNotificationServiceABC = Depends(),
    status: NotificationStatus | None = None,
    filter_by: NotificationChannelType | None = None,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
):
    return await notification_service.search_notifications_by_id(
        user_id=user_id,
        status=status,
        channel_type=filter_by,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/filter",
    description="Отображение отфильтрованного"
    " списка заданий об уведомлении для конкретного пользователя ",
    response_model=list[UserNotificationTaskSchema],
    response_description="Список заданий на уведомление",
    tags=["Пользователи"],
)
async def filter_user_notifications(
    notification_service: UserNotificationServiceABC = Depends(),
    status: NotificationStatus | None = None,
    channel_type: NotificationChannelType | None = None,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
):
    return await notification_service.get_all_channel_notifications(
        channel_type=channel_type,
        status=status,
        skip=skip,
        limit=limit,
    )
