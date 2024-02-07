from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi_limiter.depends import RateLimiter
from src.core.config import settings
from src.models.user import User
from src.schemas.auth import RefreshRequestDto, UserLoginDto
from src.schemas.result import GenericResult
from src.schemas.token import Token
from src.schemas.user import UserBase, UserCreateDto
from src.services.auth import AuthServiceABC
from src.services.user import UserServiceABC
from starlette.responses import JSONResponse

router = APIRouter()


@router.post(
    "/register",
    response_model=UserBase,
    description="Регистрация нового пользователя",
    tags=["Авторизация"],
    summary="Создание аккаунта для нового пользователя",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.rate_limit_requests_per_interval,
                seconds=settings.requests_interval,
            )
        )
    ],
)
async def register(
    user: UserCreateDto, user_service: UserServiceABC = Depends()
) -> UserBase:
    response: GenericResult[User] = await user_service.create_user(user_dto=user)
    if response.is_success:
        return response.response
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail=response.error.reason
    )


@router.post(
    "/login",
    response_model=Token,
    description="Авторизация пользователя",
    tags=["Авторизация"],
    summary="Авторизация с использование JWT",
    response_description="Пара токенов access и refresh",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.rate_limit_requests_per_interval,
                seconds=settings.requests_interval,
            )
        )
    ],
)
async def login(
    user_login: UserLoginDto,
    user_agent: Annotated[str | None, Header()] = None,
    auth: AuthServiceABC = Depends(),
):
    token: GenericResult[Token] = await auth.login(
        login=user_login.login,
        password=user_login.password,
        user_agent=user_agent,
    )
    if not token.is_success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="login or/and password incorrect"
        )

    return token.response


@router.post(
    "/refresh",
    response_model=Token,
    description="Выдача новых токенов,  если access token устарел",
    tags=["Авторизация"],
    response_description="Пара токенов access и refresh",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.rate_limit_requests_per_interval,
                seconds=settings.requests_interval,
            )
        )
    ],
)
async def refresh(
    token: RefreshRequestDto,
    auth_service: AuthServiceABC = Depends(),
):
    return await auth_service.refresh(token.jti)


@router.post(
    "/logout",
    description="Выход из аккаунта пользователя",
    tags=["Авторизация"],
)
async def logout(auth_service: AuthServiceABC = Depends()):
    await auth_service.logout()
    return JSONResponse(status_code=HTTPStatus.OK, content={})
