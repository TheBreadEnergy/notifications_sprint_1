from abc import ABC, abstractmethod
from typing import Any, List

from faker import Faker
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from src.models.user import SocialAccount, SocialNetworksEnum, User
from src.models.user_history import UserHistory
from src.schemas.result import Error, GenericResult
from src.schemas.user import (
    SocialCreateDto,
    SocialUser,
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
from src.services.event_handler import EventHandlerABC


class UserRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def get_by_login(self, *, login: str) -> User:
        ...

    @abstractmethod
    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> List[UserHistory]:
        ...

    @abstractmethod
    async def get_user_social(
        self, *, social_name: SocialNetworksEnum, social_id: str
    ) -> SocialAccount:
        ...

    @abstractmethod
    async def insert_user_login(
        self, *, user_id: Any, enter_data: UserHistoryCreateDto
    ) -> GenericResult[UserHistory]:
        ...

    @abstractmethod
    async def insert_user_social(
        self, *, user_id: Any, enter_data: SocialCreateDto
    ) -> GenericResult[SocialAccount]:
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

    async def get_user_social(
        self, *, social_name: SocialNetworksEnum, social_id: str
    ) -> SocialAccount | None:
        statement = select(SocialAccount).where(
            and_(
                SocialAccount.social_name == social_name,
                SocialAccount.social_id == social_id,
            ),
        )
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()

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

    async def insert_user_social(
        self, *, user_id: Any, enter_data: SocialCreateDto
    ) -> GenericResult[SocialAccount]:
        user: User = await self.get(entity_id=user_id)
        if not user:
            GenericResult.failure(
                error=Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
        social = SocialAccount(**enter_data.model_dump())
        user.add_social_account(social)
        return GenericResult.success(social)


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

    async def get_user_social(
        self, *, social_name: SocialNetworksEnum, social_id: str
    ) -> SocialAccount | None:
        return await self._user_repository.get_user_social(
            social_name=social_name, social_id=social_id
        )

    async def insert_user_login(
        self, *, user_id: Any, enter_data: UserHistoryCreateDto
    ) -> GenericResult[UserHistory]:
        return await self._user_repository.insert_user_login(
            user_id=user_id, enter_data=enter_data
        )

    async def insert_user_social(
        self, *, user_id: Any, enter_data: SocialCreateDto
    ) -> GenericResult[SocialAccount]:
        return await self._user_repository.insert_user_social(enter_data=enter_data)


class UserServiceABC(ABC):
    @abstractmethod
    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> list[UserHistory]:
        ...

    @abstractmethod
    async def get_users(self, *, skip: int, limit: int) -> list[User]:
        ...

    @abstractmethod
    async def update_password(
        self, *, user_id: Any, password_user: UserUpdatePasswordDto
    ) -> GenericResult[User]:
        ...

    @abstractmethod
    async def create_user(
        self, user_dto: UserCreateDto, event_handler: EventHandlerABC | None = None
    ) -> GenericResult[User]:
        ...

    @abstractmethod
    async def insert_user_login(
        self, *, user_id: Any, history_row: UserHistoryCreateDto
    ):
        ...

    @abstractmethod
    async def get_user(self, *, user_id: Any) -> GenericResult[User]:
        ...

    @abstractmethod
    async def get_user_by_login(self, *, login: str) -> User | None:
        ...

    @abstractmethod
    async def get_or_create_user(self, *, social: SocialUser) -> GenericResult[User]:
        ...

    @abstractmethod
    async def update_user(
        self, user_id: Any, user_dto: UserUpdateDto
    ) -> GenericResult[User]:
        ...

    @abstractmethod
    async def delete_user(self, *, user_id: Any) -> None:
        ...


class UserService(UserServiceABC):
    def __init__(self, repository: UserRepositoryABC, uow: UnitOfWork):
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

    async def create_user(
        self, user_dto: UserCreateDto, event_handler: EventHandlerABC | None = None
    ) -> GenericResult[User]:
        user = await self._repository.get_by_login(login=user_dto.login)
        response = GenericResult.failure(
            Error(error_code="USER_ALREADY_EXISTS", reason="User already exists")
        )
        if not user:
            user = await self._repository.insert(body=user_dto)
            await self._uow.commit()
            if event_handler:
                await event_handler.handle_registration(user_id=user.id)
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

    async def get_or_create_user(self, *, social: SocialUser) -> GenericResult[User]:
        social_user = await self._repository.get_user_social(
            social_name=social.social_name, social_id=social.id
        )
        if not social_user:
            auto_password = Faker().password()
            user = await self.get_user_by_login(login=social.login)
            if user:
                return GenericResult.failure(
                    Error(error_code="USER_EXISTS", reason="User already exists")
                )
            user_dto = UserCreateDto(
                password=auto_password,
                login=social.login,
                first_name=social.first_name,
                last_name=social.last_name,
                email=social.email,
            )
            user = await self._repository.insert(body=user_dto)
            user.add_social_account(
                social_account=SocialAccount(
                    social_id=social.id, social_name=social.social_name
                )
            )
            await self._uow.commit()
            return GenericResult.success(user)
        return await self.get_user(user_id=social_user.user_id)

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
