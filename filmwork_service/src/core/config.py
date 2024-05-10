import os

import backoff
import elasticsearch
import redis
from aiohttp import ClientConnectorError
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger
from src.errors.rate_limit import RateLimitException


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "Read-only API для онлайн-кинотеатра", alias="PROJECT_NAME", env="PROJECT_NAME"
    )
    description: str = Field(
        "Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST", env="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT", env="REDIS_PORT")
    elastic_host: str = Field("127.0.0.1", alias="ELASTIC_HOST", env="ELASTIC_HOST")
    elastic_port: int = Field(9200, alias="ELASTIC_PORT", env="ELASTIC_PORT")
    backoff_max_retries: int = Field(
        5, alias="BACKOFF_MAX_RETRIES", env="BACKOFF_MAX_RETRIES"
    )
    auth_profile: str = Field(
        "http://auth-api:8000/api/v1/users/info",
        alias="AUTH_PROFILE",
        env="AUTH_PROFILE",
    )

    # Logging settings
    log_level: str = "INFO"
    logger_filename: str = "/opt/logs/film-api-logs.json"
    logger_maxbytes: int = 15000000
    logger_mod: str = "a"
    logger_backup_count: int = 5

    sentry_dsn: str | None = None

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()


BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": (
        ClientConnectorError,
        RateLimitException,
        redis.ConnectionError,
        redis.TimeoutError,
        elasticsearch.ConnectionError,
        elasticsearch.ConnectionTimeout,
    ),
    "logger": logger,
    "max_tries": settings.backoff_max_retries,
}
