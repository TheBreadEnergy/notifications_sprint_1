import logging
from pathlib import Path

import backoff
from aiohttp import ClientConnectorError
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.errors.rate_limit import RateLimitException
from src.rate.rate_limiter import is_circuit_processable


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "API для управления закладками, лайками, рецензиями",
        alias="PROJECT_NAME",
        env="PROJECT_NAME",
    )
    description: str = Field(
        "Создание, добавление, редактирование, удаление закладок, лайков, рецензий  ",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    base_dir: str = str(Path(__file__).parent.parent)
    mongo_conn: str = Field(
        "mongos://localhost:27017", alias="MONGO_CONN", env="MONGO_CONN"
    )
    bookmarks_database: str = Field(
        "bookmarks", alias="BOOKMARKS_DATABASE", env="BOOKMARKS_DATABASE"
    )
    jaeger_endpoint_host: str = Field(
        "localhost:4317", alias="JAEGER_ENDPOINT_HOST", env="JAEGER_ENDPOINT_HOST"
    )
    auth_service: str = Field(
        "http://localhost:81", alias="AUTH_SERVICE", env="AUTH_SERVICE"
    )


settings = Settings()

logger = logging.getLogger(__name__)

BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": (ClientConnectorError, RateLimitException),
    "logger": logger,
    "max_tries": settings.backoff_max_retries,
}


CIRCUIT_CONFIG = {"expected_exception": is_circuit_processable}
