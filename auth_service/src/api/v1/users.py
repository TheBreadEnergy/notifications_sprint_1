import uuid
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.user import User
from src.schemas.result import GenericResult, Result
from src.schemas.role import Roles
from src.schemas.token import TokenValidation
from src.schemas.user import UserBase, UserDto, UserHistoryDto, UserUpdateDto
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
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
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
    result = await auth_service.get_user()
    return result


@router.get(
    "/profile/history",
    description="Вывод истории авторизаций пользователя",
    response_model=list[UserHistoryDto],
    response_description="Список авторизаций пользователя",
    tags=["Пользователи"],
    summary="Вывод истории авторизаций пользователя",
)
async def get_user_profile_history(
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
):
    user = await auth_service.get_user()
    result = await user_service.get_user_history(
        user_id=user.id, skip=skip, limit=limit
    )
    return result


@router.get(
    "/{user_id}/history",
    description="Вывод истории авторизаций пользователя",
    response_model=list[UserHistoryDto],
    response_description="Список авторизаций пользователя",
    tags=["Администратор"],
    summary="Вывод истории авторизаций пользователя",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_user_history(
    user_id: uuid.UUID,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    result = await user_service.get_user_history(
        user_id=user_id, skip=skip, limit=limit
    )
    return result


@router.get(
    "/{user_id}",
    description="Вывод информации о пользователе. Требует административных прав",
    response_model=UserDto,
    tags=["Администратор"],
    response_description="Сведения о зарегистрированном пользователе",
    summary="Сведения об учетной записи пользователя. Административный функционал",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_user(
    user_id: UUID,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
) -> User:
    user: GenericResult[User] = await user_service.get_user(user_id=user_id)
    if not user.is_success:
        raise HTTPException(status_code=400, detail=user.error.reason)
    return user.response


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
    user_result: GenericResult[User] = await user_service.update_user(
        user_id=user.id, user_dto=user_info
    )
    if not user_result.is_success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=user.error.reason
        )
    return user_result.response


@router.put(
    "/{user_id}/role/{role_id}",
    description="Добавление роли пользователю",
    tags=["Администратор"],
    summary="Назначение пользователю дополнительной роли",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
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
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
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


@router.post(
    "/info",
    description="Получение сведений о зарегистрированном пользователе по заданному"
    " jwt токену",
    summary="Получение данных о пользователе",
    tags=["Пользователи"],
)
async def get_user_data(
    token_data: TokenValidation, auth_service: AuthServiceABC = Depends()
) -> UserDto:
    user = await auth_service.get_auth_user(token_data.access_token)
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    return user


@router.delete(
    "/profile",
    description="Удаление аккаунта пользователя",
    summary="Удаление учетной записи пользователя",
    tags=["Пользователи"],
)
async def delete_user_profile(
    user_service: UserServiceABC = Depends(), auth_service: AuthServiceABC = Depends()
):
    user = await auth_service.get_user()
    await user_service.delete_user(user_id=user.id)
    await auth_service.logout()
    return JSONResponse(status_code=HTTPStatus.OK, content={})


@router.delete(
    "/{user_id}",
    description="Удаление учетной записи пользователя. Требуются права администратора.",
    summary="Удаление учетной записи пользователя",
    tags=["Администратор"],
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def delete_user(
    user_id: UUID,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    await user_service.delete_user(user_id=user_id)
    return JSONResponse(status_code=HTTPStatus.OK, content={})
