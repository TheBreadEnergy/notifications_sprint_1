from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from src.core.config import Roles
from src.models.role import Role
from src.schemas.result import GenericResult
from src.schemas.role import RoleBase, RoleCreateDto, RoleDto, RoleUpdateDto
from src.services.auth import AuthServiceABC, require_roles
from src.services.role import RoleServiceABC

router = APIRouter()


@router.get(
    "/",
    response_model=list[RoleBase],
    tags=["Роли", "Администратор"],
    description="Вывод существующих ролей системы",
    response_description="Сведения о доступных ролях системы",
    summary="Вывод существующих ролей системы",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def get_roles(
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
) -> list[RoleBase]:
    return await role_service.get_roles(skip=skip, limit=limit)


@router.get(
    "/{role_id}",
    response_model=RoleDto,
    summary="Выдача сведений о роли",
    tags=["Роли", "Администратор"],
    description="Выдача сведений о роли",
    response_description="Сведения о роли в системе",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def get_role(
    role_id: Any,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
) -> RoleDto:
    role: GenericResult[Role] = await role_service.get_role(role_id=role_id)
    if not role.is_success:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=role.error.reason)
    return role.response


@router.post(
    "/",
    response_model=RoleDto,
    description="Создание роли в системе",
    response_description="Сведения о новой роли",
    tags=["Роли", "Администратор"],
    summary="Создание роли в системе",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def create_role(
    role_data: RoleCreateDto,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    result = await role_service.create_role(role=role_data)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error.reason)
    return result.response


@router.put(
    "/{role_id}",
    response_model=RoleDto,
    description="Редактирование роли в системе",
    response_description="Отредактированная роль",
    tags=["Роли", "Администратор"],
    summary="Редактирование роли",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def update_role(
    role_id: Any,
    role_data: RoleUpdateDto,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    result = await role_service.update_role(role_id=role_id, role_dto=role_data)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error.reason)


@router.delete(
    "/{role_id}",
    response_model=RoleDto,
    description="Удаление роли из системы",
    tags=["Роли", "Администратор"],
    summary="Удаление роли из системы",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def delete_role(
    role_id: Any,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await role_service.delete_role(role_id=role_id)
