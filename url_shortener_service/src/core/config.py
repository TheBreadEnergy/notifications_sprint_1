from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".")
    echo: bool = Field(True, alias="ECHO", env="ECHO")
    project_name: str = Field(
        "API для сокращения ссылок",
        alias="PROJECT_NAME",
        env="PROJECT_NAME",
    )
    description: str = Field(
        "Сокращение и редирект на правильные ссылки",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    cache_host: str = Field("localhost", alias="CACHE_HOST", env="REDIS_HOST")
    cache_port: int = Field("6379", alias="CACHE_PORT", env="CACHE_PORT")
    base_dir: str = str(Path(__file__).parent.parent)
    postgres_conn: PostgresDsn = Field(
        "postgresql+asyncpg://app:123qwe@localhost:5432/links",
        alias="DATABASE_CONN",
        env="DATABASE_CONN",
    )
    rate_limit_requests_per_interval: int = Field(
        1,
        alias="RATE_LIMIT_REQUESTS_PER_INTERVAL",
        env="RATE_LIMIT_REQUESTS_PER_INTERVAL",
    )
    requests_interval: int = Field(
        1, alias="REQUESTS_INTERVAL", env="REQUESTS_INTERVAL"
    )
    jaeger_endpoint_host: str = Field(
        "localhost:4317", alias="JAEGER_ENDPOINT_HOST", env="JAEGER_ENDPOINT_HOST"
    )
    activation_root_url: str = Field(
        "http://auth-api:80/api/v1/accounts/activation/",
        alias="ACTIVATION_ROOT_URL",
        env="ACTIVATION_ROOT_URL",
    )
    long_live_seconds: int = Field(3600, alias="LONG_LIVE_SECS", env="LONG_LIVE_SECS")

    debug: bool = Field(True, alias="DEBUG", env="DEBUG")
    enable_tracer: bool = Field(False, alias="ENABLE_TRACER", env="ENABLE_TRACER")
    enable_limiter: bool = Field(True, alias="ENABLE_LIMITER", env="ENABLE_LIMITER")
    log_level: str = "INFO"
    logger_filename: str = "/opt/logs/shortener-api-logs.json"
    logger_maxbytes: int = 15000000
    logger_mod: str = "a"
    logger_backup_count: int = 5

    sentry_dsn: str | None = None


settings = Settings()
