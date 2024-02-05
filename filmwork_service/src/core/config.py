import logging
import os
from logging import config as logging_config

import backoff
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.logger import LOGGING


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
    auth_server: str = Field(
        "http://auth-api:8000/api/v1", alias="AUTH_HOST", env="AUTH_HOST"
    )
    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)


BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "logger": logger,
    "max_tries": settings.backoff_max_retries,
}
