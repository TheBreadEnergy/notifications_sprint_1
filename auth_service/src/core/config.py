import os
from enum import Enum

from async_fastapi_jwt_auth import AuthJWT
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "API для управления пользователями и ролями",
        alias="PROJECT_NAME",
        env="PROJECT_NAME",
    )
    description: str = Field(
        "Создание, добавление, редактирование учетными записями пользователей",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    cache_host: str = Field("localhost", alias="CACHE_HOST", env="REDIS_HOST")
    cache_port: int = Field("6379", alias="CACHE_PORT", env="CACHE_PORT")
    base_dir: str = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    postgres_conn: PostgresDsn = Field(
        "postgresql+asyncpg://app:123qwe@localhost:5432/users",
        alias="DATABASE_CONN",
        env="DATABASE_CONN",
    )
    access_expiration_seconds: int = Field(
        3600, alias="ACCESS_EXPIRATION_SECONDS", env="EXPIRATION_SECONDS"
    )
    refresh_expiration_seconds: int = Field(
        3600, alias="REFRESH_EXPIRATION_SECONDS", env="REFRESH_EXPIRATION_SECONDS"
    )
    authjwt_secret_key: str = Field(
        "secret", alias="JWT_SECRET_KEY", env="JWT_SECRET_KEY"
    )
    authjwt_denylist_enabled: bool = False
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_access_token_expires: int = Field(
        120, alias="JWT_ACCESS_EXP_TIME", env="JWT_ACCESS_EXP_TIME"
    )  # 2 minutes
    authjwt_refresh_token_expires: int = Field(
        600, alias="JWT_REFRESH_EXP_TIME", env="JWT_REFRESH_EXP_TIME"
    )  # 5 minutes


settings = Settings()


class Roles(Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"


@AuthJWT.load_config
def get_config():
    return settings
