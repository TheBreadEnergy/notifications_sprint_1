from functools import cache

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from src.dependencies.registrator import add_factory_to_mapper
from src.services.auth import AuthService, AuthServiceABC
from src.services.cache import TokenStorageABC
from src.services.user import UserServiceABC


@add_factory_to_mapper(AuthServiceABC)
@cache
def create_auth_service(
    auth_jwt: AuthJWT = Depends(),
    token_storage: TokenStorageABC = Depends(),
    user_service: UserServiceABC = Depends(),
) -> AuthServiceABC:
    return AuthService(
        auth_jwt_service=auth_jwt,
        token_storage=token_storage,
        user_service=user_service,
    )
