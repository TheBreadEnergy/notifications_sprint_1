import uuid
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.core.config import Roles
from src.models.user import User
from src.schemas.result import GenericResult, Result
from src.schemas.user import UserBase, UserDto, UserUpdateDto
from src.services.auth import AuthServiceABC, require_roles
from src.services.role import UserRoleServiceABC
from src.services.user import UserServiceABC
from starlette.responses import JSONResponse

router = APIRouter()


@router.get(
    "/",
    description="Вывод информации о всех пользователях системы",
    response_model=list[UserBase],
    response_description="Список учетных записей пользователей системы",
    tags=["Пользователи"],
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def get_users(
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await user_service.get_users(skip=skip, limit=limit)


@router.get(
    "/profile",
    description="Вывод информации об учетной записи пользователя",
    response_model=UserDto,
    response_description="Сведения об авторизированном пользователе",
    tags=["Пользователи"],
    summary="Сведения об учетной записи пользователя",
)
async def get_user_profile(auth_service: AuthServiceABC = Depends()) -> UserDto:
    return await auth_service.get_user()


@router.get(
    "/{user_id}",
    description="Вывод информации о пользователе. Требует административных прав",
    response_model=UserDto,
    tags=["Администратор"],
    response_description="Сведения о зарегистрированном пользователе",
    summary="Сведения об учетной записи пользователя. Административный функционал",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def get_user(
    user_id: UUID,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await user_service.get_user(user_id=user_id)


@router.put(
    "/profile",
    response_model=UserDto,
    description="Обновление сведений о пользователе",
    tags=["Пользователи"],
    response_description="Обновленные учетные сведения о пользователе",
    summary="Обновление учетных сведений о пользователе",
)
async def update_user_profile(
    user_info: UserUpdateDto,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
) -> UserDto:
    user = await auth_service.get_user()
    user: GenericResult[User] = await user_service.update_user(
        user_id=user.id, user_dto=user_info
    )
    if not user.is_success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=user.error.reason
        )
    return user


@router.put(
    "/{user_id}/role/{role_id}",
    description="Добавление роли пользователю",
    tags=["Администратор"],
    summary="Назначение пользователю дополнительной роли",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def assign_role_to_user(
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    user_role_service: UserRoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    result: Result = await user_role_service.assign_role_to_user(
        user_id=user_id, role_id=role_id
    )
    if not result.is_success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=result.error.reason
        )
    return JSONResponse(status_code=HTTPStatus.OK, content={})


@router.delete(
    "/{user_id}/role/{role_id}",
    description="Отобрать роль у пользователя",
    tags=["Администратор"],
    summary="Отобрать роль у пользователя",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def remove_role_from_user(
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    user_role_service: UserRoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    result: Result = await user_role_service.remove_role_from_user(
        user_id=user_id, role_id=role_id
    )
    if not result.is_success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=result.error.reason
        )
    return JSONResponse(status_code=HTTPStatus.OK, content={})


@router.delete(
    "/profile",
    description="Удаление аккаунта пользователя",
    summary="Удаление учетной записи пользователя",
    tags=["Пользователь"],
)
async def delete_user_profile(
    user_service: UserServiceABC = Depends(), auth_service: AuthServiceABC = Depends()
):
    user = await auth_service.get_user()
    await user_service.delete_user(user_id=user.id)
    return await auth_service.logout()


@router.delete(
    "/{user_id}",
    description="Удаление учетной записи пользователя. Требуются права администратора.",
    summary="Удаление учетной записи пользователя",
    tags=["Администратор"],
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def delete_user(
    user_id: UUID,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await user_service.delete_user(user_id=user_id)
