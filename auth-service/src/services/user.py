from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.schemas.result import Error, GenericResult
from src.schemas.user import UserCreateDto, UserUpdateDto, UserUpdatePasswordDto
from src.services.base import PostgresRepository, SqlAlchemyUnitOfWork


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
    ) -> GenericResult[User]:
        ...

    @abstractmethod
    def create_user(self, user_dto: UserCreateDto) -> GenericResult[User]:
        ...

    @abstractmethod
    def get_user(self, *, user_id: Any) -> GenericResult[User]:
        ...

    @abstractmethod
    def update_user(self, user_id: Any, user_dto: UserUpdateDto) -> GenericResult[User]:
        ...

    @abstractmethod
    def delete_user(self, *, user_id: Any) -> None:
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
    ) -> GenericResult[User]:
        user: User = await self._repository.get(entity_id=user_id)
        if not user:
            return GenericResult.failure(
                error=Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
        status = user.change_password(
            old_password=password_user.old_password,
            new_password=password_user.new_password,
        )
        if status:
            await self._uow.commit()
        return user

    async def create_user(self, user_dto: UserCreateDto) -> GenericResult[User]:
        user = await self._repository.get_by_name(name=user_dto.login)
        response = GenericResult.failure(
            Error(error_code="USER_ALREADY_EXISTS", reason="User already exists")
        )
        if not user:
            user = await self._repository.insert(body=user_dto)
            await self._uow.commit()
            response = GenericResult.success(user)
        return response

    async def get_user(self, *, user_id: Any) -> GenericResult[User]:
        user = await self._repository.get(entity_id=user_id)
        return (
            GenericResult.failure(
                error=Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
            if not user
            else user
        )

    async def update_user(
        self, user_id: Any, user_dto: UserUpdateDto
    ) -> GenericResult[User]:
        user = await self._repository.get(entity_id=user_id)
        if not user:
            return GenericResult.failure(
                error=Error(
                    error_code="USER_NOT_FOUND", reason="Пользователь не найден"
                )
            )
        user.update_personal(**user_dto.model_dump())
        await self._uow.commit()
        return GenericResult.success(user)

    async def delete_user(self, *, user_id: Any) -> None:
        await self._repository.delete(entity_id=user_id)
        return await self._uow.commit()
