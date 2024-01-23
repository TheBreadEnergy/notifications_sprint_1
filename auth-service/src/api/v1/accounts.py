from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.auth import UserLoginDto, RefreshRequestDto
from src.schemas.token import Token
from src.schemas.user import UserDto, UserCreateDto
from src.services.auth import AuthServiceABC
from src.services.user import UserServiceABC

router = APIRouter()


@router.post(
    "/register",
    response_model=UserDto,
    description="Регистрация нового пользователя",
    tags=["Пользователи", "Авторизация"],
    summary="Создание аккаунта для нового пользователя",
)
async def register(user: UserCreateDto, user_service: UserServiceABC = Depends()):
    return await user_service.create_user(user_dto=user)


@router.post(
    "/login",
    response_model=Token,
    description="Авторизация пользователя",
    tags=["Пользователи", "Авторизация"],
    summary="Авторизация с использование JWT",
    response_description="Пара токенов access и refresh",
)
async def login(user_login: UserLoginDto, auth: AuthServiceABC = Depends()):
    token = await auth.login(login=user_login.login, password=user_login.password)
    if token is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="login or/and password incorrect"
        )
    return token


@router.post(
    "/refresh",
    response_model=Token,
    description="Выдача новых токенов,  если access token устарел",
    tags=["Пользователи", "Авторизация"],
    response_description="Пара токенов access и refresh",
)
async def refresh(token: RefreshRequestDto, auth_service: AuthServiceABC = Depends()):
    return await auth_service.refresh(token.jti)


@router.post(
    "/logout",
    description="Выход из аккаунта пользователя",
    tags=["Пользователи", "Авторизация"],
)
async def logout(auth_service: AuthServiceABC = Depends()):
    return await auth_service.logout()
