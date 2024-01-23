from abc import ABC, abstractmethod
from functools import wraps

from async_fastapi_jwt_auth import AuthJWT

from starlette.responses import JSONResponse

from src.core.config import settings
from src.models.user import User
from src.schemas.token import Token
from src.schemas.user import UserCreateDto
from src.services.base import PostgresRepository
from src.services.cache import TokenStorageABC


class AuthServiceABC(ABC):
    @abstractmethod
    def login(self, *, login: str, password: str) -> Token | None:
        ...

    @abstractmethod
    def logout(self):
        ...

    @abstractmethod
    def refresh(self, access_jti: str | None) -> Token | None:
        ...

    @abstractmethod
    def require_auth(self):
        ...

    @abstractmethod
    def optional_auth(self):
        ...

    @abstractmethod
    def get_user(self) -> User | None:
        ...


class AuthService(AuthServiceABC):
    def __init__(
        self,
        auth_jwt_service: AuthJWT,
        token_storage: TokenStorageABC,
        user_repository: PostgresRepository[User, UserCreateDto],
    ):
        self._auth_jwt_service = auth_jwt_service
        self._token_storage = token_storage
        self._user_repository = user_repository

    async def login(self, *, login: str, password: str) -> Token | None:
        user = await self._user_repository.get_by_name(name=login)
        if not user or not user.check_password(password):
            return None
        access_token = await self._auth_jwt_service.create_access_token(
            subject=str(user.id)
        )
        refresh_token = await self._auth_jwt_service.create_refresh_token(
            subject=str(user.id)
        )
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def logout(self) -> None:
        await self._auth_jwt_service.jwt_required()
        access_jti = (await self._auth_jwt_service.get_raw_jwt())["jti"]
        return await self._token_storage.store_token(
            key=access_jti,
            value=True,
            expiration_time=settings.access_expiration_seconds,
        )

    async def refresh(self, access_jti: str) -> Token | None:
        await self._auth_jwt_service.jwt_refresh_token_required()
        refresh_jti = (await self._auth_jwt_service.get_raw_jwt())["jti"]
        await self._token_storage.store_token(
            key=refresh_jti,
            value=True,
            expiration_time=settings.refresh_expiration_seconds,
        )
        await self._token_storage.store_token(
            key=access_jti,
            value=True,
            expiration_time=settings.access_expiration_seconds,
        )
        user_subject = await self._auth_jwt_service.get_jwt_subject()
        access_token = await self._auth_jwt_service.create_access_token(
            subject=user_subject
        )
        refresh_token = await self._auth_jwt_service.create_refresh_token(
            subject=user_subject
        )
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def require_auth(self):
        await self._auth_jwt_service.jwt_required()
        jti = (await self._auth_jwt_service.get_raw_jwt())["jti"]
        return not (await self._token_storage.check_expiration(jti))

    async def optional_auth(self):
        return await self._auth_jwt_service.jwt_optional()

    async def get_user(self) -> User | None:
        await self._auth_jwt_service.jwt_required()
        user_subject = await self._auth_jwt_service.get_jwt_subject()
        user = await self._user_repository.get(entity_id=user_subject)
        return user


def require_roles(roles: list[str]):
    def auth_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            auth_service = kwargs["auth_service"]
            current_user: User = await auth_service.get_user()
            for role in current_user.roles:
                if role.name in roles:
                    return await func(*args, **kwargs)
            return JSONResponse(
                status_code=403, content={"message": "I have not access"}
            )

        return wrapper

    return auth_decorator
