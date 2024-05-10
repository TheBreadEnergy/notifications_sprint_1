from http import HTTPStatus
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.base import NotificationStatus
from src.models.system_notification import ContentType, SystemNotificationTask
from src.schemas.api.v1.system_notification_task import SystemNotificationTaskSchema
from src.schemas.user import UserDto
from src.services.bearer import check_is_admin, security_jwt
from src.services.system_notification import SystemNotificationServiceABC

router = APIRouter()


@router.get(
    "/",
    response_model=list[SystemNotificationTaskSchema],
    response_description="Список системных задач на уведомления",
    description="Вывод всех системных задач для пользовательских уведомлений",
    tags=["Система"],
)
async def get_system_notification_tasks(
    system_notification_service: SystemNotificationServiceABC = Depends(),
    status: NotificationStatus | None = None,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> Sequence[SystemNotificationTask]:
    if not check_is_admin(user=user):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    return await system_notification_service.get_all_notifications(
        status=status,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/filter",
    response_model=list[SystemNotificationTaskSchema],
    response_description="Список системных задач на уведомление пользователей",
    description="Отображение фильтрованного списка системных задач нотификаций",
    tags=["Система"],
)
async def filter_system_notifications_task_by_type(
    system_notification_service: SystemNotificationServiceABC = Depends(),
    content_id: UUID = None,
    content_type: ContentType | None = None,
    status: Annotated[
        NotificationStatus, Query(description="Status of notification")
    ] = None,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    if not check_is_admin(user=user):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    if not content_type and not status:
        return await system_notification_service.get_all_notifications(
            status=status, skip=skip, limit=limit
        )
    if not content_id:
        return await system_notification_service.search_by_content_type(
            content_type=content_type, status=status, skip=skip, limit=limit
        )
    if not content_type:
        return await system_notification_service.search_for_content_id(
            content_id=content_id, status=status, skip=skip, limit=limit
        )
