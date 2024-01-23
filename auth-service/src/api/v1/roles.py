from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from src.core.config import Roles
from src.schemas.role import RoleBase, RoleDto, RoleCreateDto, RoleUpdateDto
from src.services.auth import require_roles, AuthServiceABC
from src.services.role import RoleServiceABC

router = APIRouter()


@router.get(
    "/",
    response_model=list[RoleBase],
    tags=["Роли"],
    description="Вывод существующих ролей системы. Требуются права администратора и выше",
    response_description="Сведения о доступных ролях системы",
    summary="Вывод существующих ролей системы. Требуются права администратора и выше",
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
    tags=["Роли"],
    description="Выдача сведений о роли",
    response_description="Сведения о роли в системе",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def get_role(
    role_id: Any,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
) -> RoleDto:
    return await role_service.get_role(role_id=role_id)


@router.post(
    "/",
    response_model=RoleDto,
    description="Создание роли в системе",
    response_description="Сведения о новой роли",
    tags=["Роли"],
    summary="Создание роли в системе",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def create_role(
    role_data: RoleCreateDto,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await role_service.create_role(role_data)


@router.put(
    "/{role_id}",
    response_model=RoleDto,
    description="Редактирование роли в системе",
    response_description="Отредактированная роль",
    tags=["Роли"],
    summary="Редактирование роли",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def update_role(
    role_id: Any,
    role_data: RoleUpdateDto,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await role_service.update_role(role_id=role_id, role_dto=role_data)


@router.delete(
    "/{role_id}",
    response_model=RoleDto,
    description="Удаление роли из системы",
    tags=["Роли"],
    summary="Удаление роли из системы",
)
@require_roles([str(Roles.ADMIN), str(Roles.SUPER_ADMIN)])
async def delete_role(
    role_id: Any,
    role_service: RoleServiceABC = Depends(),
    auth_service: AuthServiceABC = Depends(),
):
    return await role_service.delete_role(role_id=role_id)
