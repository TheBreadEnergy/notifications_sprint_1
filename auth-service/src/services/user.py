from abc import ABC, abstractmethod
from typing import Any, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserCreateDto, UserUpdatePasswordDto, UserUpdateDto
from src.services.base import PostgresRepository, SqlAlchemyUnitOfWork, ModelType


class UserRepository(PostgresRepository[User, UserCreateDto]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def get_by_name(self, *, name: str) -> User:
        statement = select(self._model).where(self._model.login == name)
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()


class UserServiceABC(ABC):
    @abstractmethod
    def get_users(self, *, skip: int, limit: int) -> list[User]:
        ...

    @abstractmethod
    def update_password(
        self, *, user_id: Any, password_user: UserUpdatePasswordDto
    ) -> User | None:
        ...

    @abstractmethod
    def create_user(self, user_dto: UserCreateDto) -> User:
        ...

    @abstractmethod
    def get_user(self, *, user_id: Any) -> User | None:
        ...

    @abstractmethod
    def update_user(self, user_id: Any, user_dto: UserUpdateDto) -> User | None:
        ...

    @abstractmethod
    def delete_user(self, *, user_id: Any):
        ...


class UserService(UserServiceABC):
    def __init__(
        self,
        repository: PostgresRepository[User, UserCreateDto],
        uow: SqlAlchemyUnitOfWork,
    ):
        self._repository = repository
        self._uow = uow

    async def get_users(self, *, skip: int, limit: int) -> list[User]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def update_password(
        self, *, user_id: Any, password_user: UserUpdatePasswordDto
    ) -> User | None:
        user: User = await self._repository.get(entity_id=user_id)
        if not user:
            return None
        status = user.change_password(
            old_password=password_user.old_password,
            new_password=password_user.new_password,
        )
        if status:
            await self._uow.commit()
        return user

    async def create_user(self, user_dto: UserCreateDto) -> User:
        user = await self._repository.insert(body=user_dto)

        await self._uow.commit()
        return user

    async def get_user(self, *, user_id: Any) -> User | None:
        return await self._repository.get(entity_id=user_id)

    async def update_user(self, user_id: Any, user_dto: UserUpdateDto) -> User | None:
        user = await self._repository.get(entity_id=user_id)
        if not user:
            return None
        user.update_personal(**user_dto.model_dump())
        await self._uow.commit()
        return user

    async def delete_user(self, *, user_id: Any) -> None:
        await self._repository.delete(entity_id=user_id)
        return await self._uow.commit()
