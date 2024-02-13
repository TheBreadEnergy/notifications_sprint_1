from http import HTTPStatus

import aiohttp
import backoff
from aiohttp import ClientConnectorError
from aiohttp.web_exceptions import HTTPError
from circuitbreaker import CircuitBreakerError, circuit
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.core.config import settings
from src.errors.rate_limit import RateLimitException
from src.schemas.token import TokenValidation


def is_rate_limited(thrown_type, thrown_value):
    return issubclass(thrown_type, HTTPError) and thrown_value.status_code == 429


def is_circuit_processable(thrown_type, thrown_value):
    return is_rate_limited(thrown_type, thrown_value) or issubclass(
        thrown_type, ClientConnectorError
    )


# TODO: place configuring in core.settings file
@backoff.on_exception(
    backoff.expo, exception=(ClientConnectorError, RateLimitException), max_tries=6
)
@circuit(expected_exception=is_circuit_processable)
async def get_user_info(token: str):
    token_payload = TokenValidation(access_token=token).model_dump(mode="json")
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url=f"{settings.auth_server}/users/info",
            json=token_payload,
            headers={"Content-Type": "application/json"},
        )
        if response.status == HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitException()
        if response.status != HTTPStatus.OK:
            raise HTTPException(status_code=response.status, detail=response.reason)
        return response.json()


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
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
    async def get_user(token: str):
        return await get_user_info(token=token)


security_jwt = JwtBearer()
