from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.core.config import Roles
from src.schemas.user import UserDto, UserUpdateDto, UserBase
from src.services.auth import require_roles, AuthServiceABC
from src.services.user import UserServiceABC

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
    tags=["Пользователи", "Администратор"],
    response_description="Сведения о зарегистрированном пользователе",
    summary="Сведения об учетной записи пользователя. Административный функционал",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def get_user(
    user_id: int,
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
    user = await user_service.update_user(user_id=user.id, user_dto=user_info)
    return user


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
    tags=["Пользователь", "Администратор"],
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def delete_user(
    user_id: int,
    user_service: UserServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await user_service.delete_user(user_id=user_id)
