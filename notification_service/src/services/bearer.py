from http import HTTPStatus

import backoff
from aiohttp import ClientSession
from circuitbreaker import CircuitBreakerError, circuit
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.core.config import BACKOFF_CONFIG, CIRCUIT_CONFIG, settings
from src.exceptions.rate_limit import RateLimitException
from src.schemas.token import TokenPayload
from src.schemas.user import Roles, UserDto


@backoff.on_exception(**BACKOFF_CONFIG)
@circuit(**CIRCUIT_CONFIG)
async def get_user_info(token: str) -> UserDto:
    token_payload = TokenPayload(access_token=token).model_dump(mode="json")
    async with ClientSession() as session:
        response = await session.post(
            url=f"{settings.auth_service}",
            json=token_payload,
            headers={"Content-Type": "application/json"},
        )
        if response.status == HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitException()
        if response.status != HTTPStatus.OK:
            raise HTTPException(status_code=response.status, detail=response.reason)
        body = await response.json()
        return UserDto(**body)


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UserDto:
        try:
            credentials: HTTPAuthorizationCredentials = await super().__call__(request)
            if not credentials:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Invalid authorization code.",
                )
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Only Bearer token might be accepted",
                )
            return await self.get_user(token=credentials.credentials)
        except CircuitBreakerError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Service unavailable"
            )

    @staticmethod
    async def get_user(token: str) -> UserDto:
        return await get_user_info(token=token)


security_jwt = JwtBearer()


def check_is_admin(user: UserDto) -> bool:
    role_names = [role_name.name for role_name in user.roles]
    return Roles.SUPER_ADMIN in role_names or Roles.ADMIN in role_names
