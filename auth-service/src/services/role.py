from abc import ABC, abstractmethod
from select import select
from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.role import Role
from src.models.user import User
from src.schemas.result import Result, Error
from src.schemas.role import RoleCreateDto, RoleUpdateDto
from src.schemas.user import UserCreateDto
from src.services.base import PostgresRepository, SqlAlchemyUnitOfWork, ModelType


class RoleRepository(PostgresRepository[Role, RoleCreateDto]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Role)

    async def get_by_name(self, *, name: str) -> Role:
        statement = select(self._model).where(self._model.name == name)
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()


class RoleServiceABC(ABC):
    @abstractmethod
    def get_roles(self, *, skip: int, limit: int) -> list[Role]:
        ...

    @abstractmethod
    def create_role(self, role: RoleCreateDto) -> Role:
        ...

    @abstractmethod
    def get_role(self, role_id: Any) -> Role | None:
        ...

    @abstractmethod
    def update_role(self, role_id: Any, role_dto: RoleUpdateDto) -> Role | None:
        ...

    @abstractmethod
    def delete_role(self, role_id: Any) -> None:
        ...


class RoleService(RoleServiceABC):
    def __init__(
        self,
        repository: PostgresRepository[Role, RoleCreateDto],
        uow: SqlAlchemyUnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def get_roles(self, *, skip: int, limit: int) -> list[Role]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def create_role(self, role: RoleCreateDto) -> Role:
        role = await self._repository.insert(body=role)
        await self._uow.commit()
        return role

    async def get_role(self, role_id: Any) -> Role | None:
        return await self._repository.get(entity_id=role_id)

    async def update_role(self, role_id: Any, role_dto: RoleUpdateDto) -> Role | None:
        role = await self._repository.get(entity_id=role_id)
        role.update_role(**role_dto.model_dump())
        await self._uow.commit()
        return role

    async def delete_role(self, role_id: Any) -> None:
        await self._repository.delete(entity_id=role_id)
        return await self._uow.commit()


class UserRoleServiceABC(ABC):
    @abstractmethod
    def assign_role_to_user(self, *, user_id: Any, role: Any) -> Result:
        ...

    @abstractmethod
    def remove_role_from_user(self, *, user_id: Any, role: Any) -> Result:
        ...


class UserRoleService(UserRoleServiceABC):
    def __init__(
        self,
        user_repository: PostgresRepository[User, UserCreateDto],
        role_repository: PostgresRepository[Role, RoleCreateDto],
        uow: SqlAlchemyUnitOfWork,
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._uow = uow

    async def assign_role_to_user(self, *, user_id: Any, role_id: Any) -> Result:
        user = await self._user_repository.get(entity_id=user_id)
        role = await self._role_repository.get(entity_id=role_id)
        if not user:
            return Result.failure(error=Error("UserNotFound", "User does not exist"))
        if not role:
            return Result.failure(error=Error("RoleNotFound", "Role does not exist"))
        user.assign_role(role)
        await self._uow.commit()
        return Result.success()

    async def remove_role_from_user(self, *, user_id: Any, role_id: Any) -> Result:
        user = await self._user_repository.get(entity_id=user_id)
        role = await self._role_repository.get(entity_id=role_id)
        if not user:
            return Result.failure(error=Error("UserNotFound", "User does not exist"))
        if not role:
            return Result.failure(error=Error("RoleNotFound", "Role does not exist"))
        user.remove_role(role)
        await self._uow.commit()
        return Result.success()
