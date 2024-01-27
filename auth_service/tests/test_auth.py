from unittest.mock import AsyncMock

import pytest
from faker import Faker
from fastapi import HTTPException
from src.api.v1.accounts import login, refresh, register
from src.models.user import User
from src.schemas.auth import RefreshRequestDto, UserLoginDto
from src.schemas.token import Token
from src.schemas.user import UserCreateDto
from src.services.auth import AuthServiceABC
from src.services.user import UserServiceABC

fake = Faker()


class MockGenericResult:
    def __init__(self, response, is_success=True):
        self.response = response
        self.is_success = is_success


# Тесты для функции регистрации
@pytest.mark.asyncio
async def test_register_success(mocker):
    user_create_dto = UserCreateDto(
        login=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )

    mock_user = User(
        login=user_create_dto.login,
        first_name=user_create_dto.first_name,
        last_name=user_create_dto.last_name,
        email=user_create_dto.email,
        password=user_create_dto.password,
    )

    mock_generic_result = MockGenericResult(response=mock_user)

    user_service_mock = mocker.MagicMock(spec=UserServiceABC)
    user_service_mock.create_user = AsyncMock(return_value=mock_generic_result)

    response = await register(user_create_dto, user_service_mock)

    assert response == mock_generic_result.response
    user_service_mock.create_user.assert_called_once_with(user_dto=user_create_dto)


# Тест на успешный вход в систему
@pytest.mark.asyncio
async def test_login_success(mocker):
    user_login_dto = UserLoginDto(login=fake.user_name(), password=fake.password())

    mock_token = MockGenericResult(
        response=Token(
            access_token="mock_access_token", refresh_token="mock_refresh_token"
        )
    )

    auth_service_mock = mocker.MagicMock(spec=AuthServiceABC)
    auth_service_mock.login = AsyncMock(return_value=mock_token)

    response = await login(user_login_dto, None, auth_service_mock)

    assert response == mock_token.response
    auth_service_mock.login.assert_called_once_with(
        login=user_login_dto.login, password=user_login_dto.password, user_agent=None
    )


# Тест на неудачный вход в систему
@pytest.mark.asyncio
async def test_login_failure(mocker):
    user_login_dto = UserLoginDto(login=fake.user_name(), password=fake.password())

    auth_service_mock = mocker.MagicMock(spec=AuthServiceABC)
    auth_service_mock.login.side_effect = HTTPException(
        status_code=401, detail="Incorrect login or password"
    )

    with pytest.raises(HTTPException) as exc_info:
        await login(user_login_dto, None, auth_service_mock)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect login or password"
    auth_service_mock.login.assert_called_once_with(
        login=user_login_dto.login, password=user_login_dto.password, user_agent=None
    )


# Тест на успешное обновление токена
@pytest.mark.asyncio
async def test_refresh_success(mocker):
    refresh_request_dto = RefreshRequestDto(jti=fake.uuid4())

    new_mock_token = Token(
        access_token="new_mock_access_token", refresh_token="new_mock_refresh_token"
    )

    auth_service_mock = mocker.MagicMock(spec=AuthServiceABC)
    auth_service_mock.refresh = AsyncMock(return_value=new_mock_token)

    response = await refresh(refresh_request_dto, auth_service_mock)

    assert response == new_mock_token
    auth_service_mock.refresh.assert_called_once_with(refresh_request_dto.jti)
