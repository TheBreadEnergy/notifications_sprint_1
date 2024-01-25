from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.role import Role
from src.models.user import User
from src.schemas.result import Error, GenericResult, Result
from src.schemas.role import RoleCreateDto, RoleUpdateDto
from src.schemas.user import UserCreateDto
from src.services.base import (
    CachedRepository,
    PostgresRepository,
    RepositoryABC,
    SqlAlchemyUnitOfWork,
)
from src.services.cache import CacheServiceABC


class RoleRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    def get_role_by_name(self, *, name: str) -> Role | None:
        ...


class RoleRepository(PostgresRepository[Role, RoleCreateDto], RoleRepositoryABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Role)

    async def get_role_by_name(self, *, name: str) -> Role | None:
        statement = select(self._model).where(self._model.name == name)
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()


class CachedRoleRepository(CachedRepository[Role, RoleCreateDto], RoleRepositoryABC):
    def __init__(self, repository: RoleRepositoryABC, cache_service: CacheServiceABC):
        super().__init__(repository=repository, cache_service=cache_service, model=Role)
        self._role_repository = repository

    async def get_role_by_name(self, *, name: str) -> User:
        key = f"{self._model.__name__}_{name}"
        entity = await self._cache.get(key=key)
        if not entity:
            entity = await self._role_repository.get_role_by_name(name=name)
        return entity


class RoleServiceABC(ABC):
    @abstractmethod
    def get_roles(self, *, skip: int, limit: int) -> list[Role]:
        ...

    @abstractmethod
    def create_role(self, role: RoleCreateDto) -> GenericResult[Role]:
        ...

    @abstractmethod
    def get_role(self, role_id: Any) -> GenericResult[Role]:
        ...

    @abstractmethod
    def update_role(self, role_id: Any, role_dto: RoleUpdateDto) -> GenericResult[Role]:
        ...

    @abstractmethod
    def delete_role(self, role_id: Any) -> None:
        ...


class RoleService(RoleServiceABC):
    def __init__(
        self,
        repository: RoleRepositoryABC,
        uow: SqlAlchemyUnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def get_roles(self, *, skip: int, limit: int) -> list[Role]:
        result = await self._repository.gets(skip=skip, limit=limit)
        return result

    async def create_role(self, role: RoleCreateDto) -> GenericResult[Role]:
        role_db = await self._repository.get_role_by_name(name=role.name)
        response = GenericResult.failure(
            Error(error_code="ROLE_ALREADY_EXISTS", reason="Role already exists")
        )
        if not role_db:
            role = await self._repository.insert(body=role)
            await self._uow.commit()
            response = GenericResult.success(role)
        return response

    async def get_role(self, role_id: Any) -> GenericResult[Role]:
        role = await self._repository.get(entity_id=role_id)
        return (
            GenericResult.success(role)
            if role
            else GenericResult.failure(
                error=Error(error_code="ROLE_NOT_FOUND", reason="Role not found")
            )
        )

    async def update_role(
        self, role_id: Any, role_dto: RoleUpdateDto
    ) -> GenericResult[Role]:
        role = await self._repository.get(entity_id=role_id)
        response = GenericResult.failure(
            error=Error(error_code="ROLE_NOT_FOUND", reason="Role not found")
        )
        if role:
            role.update_role(**role_dto.model_dump())
            await self._uow.commit()
            response = GenericResult.success(role)
        return response

    async def delete_role(self, role_id: Any) -> None:
        await self._repository.delete(entity_id=role_id)
        return await self._uow.commit()


class UserRoleServiceABC(ABC):
    @abstractmethod
    def assign_role_to_user(self, *, user_id: Any, role_id: Any) -> Result:
        ...

    @abstractmethod
    def remove_role_from_user(self, *, user_id: Any, role_id: Any) -> Result:
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
