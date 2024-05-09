from http import HTTPStatus
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.base import NotificationStatus
from src.models.user_notification import NotificationChannelType, UserNotificationTask
from src.schemas.api.v1.user_notification_task import UserNotificationTaskSchema
from src.schemas.user import UserDto
from src.services.bearer import check_is_admin, security_jwt
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
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> Sequence[UserNotificationTask]:
    if not check_is_admin(user=user):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
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
    channel_type: NotificationChannelType | None = None,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    if user.id != user_id and not check_is_admin(user=user):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    return await notification_service.search_notifications_by_id(
        user_id=user_id,
        status=status,
        channel_type=channel_type,
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
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    if not check_is_admin(user=user):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    return await notification_service.get_all_channel_notifications(
        channel_type=channel_type,
        status=status,
        skip=skip,
        limit=limit,
    )
