import os

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
    rate_limit_requests_per_interval: int = Field(
        1,
        alias="RATE_LIMIT_REQUESTS_PER_INTERVAL",
        env="RATE_LIMIT_REQUESTS_PER_INTERVAL",
    )
    requests_interval: int = Field(
        1, alias="REQUESTS_INTERVAL", env="REQUESTS_INTERVAL"
    )
    jaeger_agent_host: str = Field(
        "localhost", alias="JAEGER_AGENT_HOST", env="JAEGER_AGENT_HOST"
    )
    jaeger_agent_port: int = Field(
        4317, alias="JAEGER_AGENT_PORT", env="JAEGER_AGENT_PORT"
    )
    authjwt_secret_key: str = Field(
        "secret", alias="JWT_SECRET_KEY", env="JWT_SECRET_KEY"
    )
    echo: bool = Field(True, alias="ECHO", env="ECHO")
    authjwt_denylist_enabled: bool = False
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_access_token_expires: int = Field(
        3600, alias="JWT_ACCESS_EXP_TIME", env="JWT_ACCESS_EXP_TIME"
    )  # 2 minutes
    authjwt_refresh_token_expires: int = Field(
        3600, alias="JWT_REFRESH_EXP_TIME", env="JWT_REFRESH_EXP_TIME"
    )  # 5 minutes
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_same_site: str = "lax"

    social_auth_redirect_url: str = Field(
        "http://localhost:8000/api/v1/socials",
        alias="SOCIAL_AUTH_URL",
        env="SOCIAL_AUTH_URL",
    )

    yandex_client_id: str = Field(
        "27cf19fb151f460ba90f92a028ea829a",
        alias="YANDEX_CLIENT_ID",
        env="YANDEX_CLIENT_ID",
    )
    yandex_client_secret: str = Field(
        "853c761b0b0f4d3896c5f58fc1f9eff4",
        alias="YANDEX_CLIENT_SECRET",
        env="YANDEX_CLIENT_SECRET",
    )
    yandex_auth_base_url: str = Field(
        "https://oauth.yandex.ru/authorize",
        alias="YANDEX_AUTH_BASE_URL",
        env="YANDEX_AUTH_BASE_URL",
    )
    yandex_auth_token_url: str = Field(
        "https://oauth.yandex.ru/token",
        alias="YANDEX_AUTH_TOKEN_URL",
        env="YANDEX_TOKEN_URL",
    )
    yandex_userinfo_url: str = Field(
        "https://login.yandex.ru/info",
        alias="YANDEX_USERINFO_URL",
        env="YANDEX_USERINFO_URL",
    )

    google_client_id: str = Field("", alias="GOOGLE_CLIENT_ID", env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(
        "", alias="GOOGLE_CLIENT_SECRET", env="GOOGLE_CLIENT_SECRET"
    )
    google_auth_base_url: str = Field(
        "https://accounts.google.com/o/oauth2/v2/auth",
        alias="GOOGLE_AUTH_BASE_URL",
        env="GOOGLE_AUTH_BASE_URL",
    )
    google_auth_token_url: str = Field(
        "ttps://www.googleapis.com/oauth2/v4/token",
        alias="GOOGLE_AUTH_TOKEN_URL",
        env="GOOGLE_AUTH_TOKEN_URL",
    )
    google_userinfo_url: str = Field(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        alias="GOOGLE_USERINFO_URL",
        env="GOOGLE_USERINFO_URL",
    )


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
