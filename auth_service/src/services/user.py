from abc import ABC, abstractmethod
from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from src.models.user import User
from src.models.user_history import UserHistory
from src.schemas.result import Error, GenericResult
from src.schemas.user import (
    UserCreateDto,
    UserHistoryCreateDto,
    UserUpdateDto,
    UserUpdatePasswordDto,
)
from src.services.base import (
    CachedRepository,
    ModelType,
    PostgresRepository,
    RepositoryABC,
    UnitOfWork,
)
from src.services.cache import CacheServiceABC


class UserRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    def get_by_login(self, *, login: str) -> User:
        ...

    @abstractmethod
    def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> List[UserHistory]:
        ...

    @abstractmethod
    def insert_user_login(self, *, user_id: str, enter_data: UserHistoryCreateDto):
        ...


class UserRepository(PostgresRepository[User, UserCreateDto], UserRepositoryABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def get_by_login(self, *, login: str) -> User:
        statement = select(self._model).where(self._model.login == login)
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()

    async def get(self, *, entity_id: Any) -> ModelType:
        statement = (
            select(self._model)
            .options(noload(self._model.history))
            .options(selectinload(self._model.roles))
            .where(self._model.id == entity_id)
        )
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()

    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> List[UserHistory]:
        statement = (
            select(UserHistory)
            .where(UserHistory.user_id == user_id)
            .order_by()
            .offset(skip)
            .limit(limit)
        )
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def insert_user_login(
        self, *, user_id: Any, enter_data: UserHistoryCreateDto
    ) -> GenericResult[UserHistory]:
        user = await self.get(entity_id=user_id)
        if not user:
            GenericResult.failure(
                error=Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
        user_history = UserHistory(**enter_data.model_dump())
        user.add_user_session(user_history)
        return GenericResult.success(user_history)


class CachedUserRepository(CachedRepository[User, UserCreateDto], UserRepositoryABC):
    def __init__(self, repository: UserRepositoryABC, cache_service: CacheServiceABC):
        super().__init__(repository=repository, cache_service=cache_service, model=User)
        self._user_repository = repository

    async def get_by_login(self, *, login: str) -> User:
        key = f"{self._model.__name__}_{login}"
        entity = await self._cache.get(key=key)
        if not entity:
            entity = await self._user_repository.get_by_login(login=login)
        return entity

    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> List[UserHistory]:
        return await self._user_repository.get_user_history(
            user_id=user_id, skip=skip, limit=limit
        )

    async def insert_user_login(
        self, *, user_id: str, enter_data: UserHistoryCreateDto
    ):
        return await self._user_repository.insert_user_login(
            user_id=user_id, enter_data=enter_data
        )


class UserServiceABC(ABC):
    @abstractmethod
    def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> list[UserHistory]:
        ...

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
    def insert_user_login(self, *, user_id: Any, history_row: UserHistoryCreateDto):
        ...

    @abstractmethod
    def get_user(self, *, user_id: Any) -> GenericResult[User]:
        ...

    @abstractmethod
    def get_user_by_login(self, *, login: str) -> User | None:
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
        repository: UserRepositoryABC,
        uow: UnitOfWork,
    ):
        self._repository = repository
        self._uow = uow

    async def get_users(self, *, skip: int, limit: int) -> list[User]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> list[UserHistory]:
        return await self._repository.get_user_history(
            user_id=user_id, skip=skip, limit=limit
        )

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
        user = await self._repository.get_by_login(login=user_dto.login)
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
            else GenericResult.success(user)
        )

    async def get_user_by_login(self, *, login: str) -> User | None:
        user = await self._repository.get_by_login(login=login)
        return user

    async def insert_user_login(
        self, *, user_id: Any, history_row: UserHistoryCreateDto
    ) -> GenericResult[UserHistory]:
        result = await self._repository.insert_user_login(
            user_id=user_id, enter_data=history_row
        )
        if result.is_success:
            await self._uow.commit()
        return result

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
