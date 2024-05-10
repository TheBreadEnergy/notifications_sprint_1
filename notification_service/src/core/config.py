import os

import backoff
from aiohttp import ClientConnectorError
from loguru import logger
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.exceptions.rate_limit import RateLimitException
from src.rate.rate_limiter import is_circuit_processable


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "API для просмотра истории нотификаций",
        alias="PROJECT_NAME",
        env="PROJECT_NAME",
    )
    description: str = Field(
        "Просмотр и отмена выбранных уведомлений",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    postgres_conn: PostgresDsn = Field(
        "postgresql+asyncpg://app:123qwe@localhost:5432/notifications",
        alias="DATABASE_CONN",
        env="DATABASE_CONN",
    )
    jaeger_endpoint_host: str = Field(
        "localhost:4317", alias="JAEGER_ENDPOINT_HOST", env="JAEGER_ENDPOINT_HOST"
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    rabbit_login: str = Field("admin", alias="RABBIT_LOGIN", env="RABBIT_LOGIN")
    rabbit_password: str = Field(
        "password", alias="RABBIT_PASSWORD", env="RABBIT_PASSWORD"
    )
    grpc_port: int = Field(50051, alias="GRPC_PORT", env="GRPC_PORT")
    rabbit_host: str = Field("localhost", alias="RABBIT_HOST", env="RABBIT_HOST")
    rabbit_port: int = Field(5672, alias="RABBIT_PORT", env="RABBIT_PORT")
    queue_name: str = Field("workers", alias="QUEUE_NAME", env="QUEUE_NAME")
    queue_waiting: str = Field(
        "workers-waiting", alias="QUEUE_WAITING", env="QUEUE_WAITING"
    )
    queue_retry: str = Field("workers-retry", alias="QUEUE_RETRY", env="QUEUE_RETRY")
    default_ttl_ms: int = Field(500, alias="DEFAULT_TTL", env="DEFAULT_TTL")
    delayed_exchange: str = Field(
        "workers-exchange-delay", alias="DELAYED_EXCHANGE", env="DELAYED_EXCHANGE"
    )
    incoming_exchange: str = Field(
        "workers-exchange-incoming", alias="DELAYED_EXCHANGE", env="DELAYED_EXCHANGE"
    )
    sorting_exchange: str = Field(
        "workers-exchange-sorting", alias="SORTING_EXCHANGE", env="SORTING_EXCHANGE"
    )
    retry_exchange: str = Field("workers-exchange-retry", alias="RETRY_EXCHANGE")

    register_routing_key: str = Field(
        "send-welcome", alias="REGISTER_ROUTING_KEY", env="REGISTER_ROUTING_KEY"
    )
    activating_routing_key: str = Field(
        "send-activating", alias="ACTIVATING_ROUTING_KEY", env="ACTIVATING_ROUTING_KEY"
    )
    long_no_see_routing_key: str = Field(
        "long_no_see", alias="LONG_NOSE_ROUTING_KEY", env="LONG_NOSE_ROUTING_KEY"
    )

    film_routing_key: str = Field(
        "film-published", alias="FILM_ROUTING_KEY", env="FILM_ROUTING_KEY"
    )
    bookmark_routing_key: str = Field(
        "bookmark-remainder", alias="BOOKMARK_ROUTING_KEY", env="BOOKMARK_ROUTING_KEY"
    )
    message_routing_key: str = Field(
        "managers-messages", alias="MESSAGE_ROUTING_KEY", env="MESSAGE_ROUTING_KEY"
    )
    routing_prefix: str = Field(
        "workers", alias="MESSAGE_VERSION", env="MESSAGE_VERSION"
    )
    supported_message_versions: list[str] = ["v1"]

    auth_service: str = Field(
        "http://localhost:8001/api/v1/users/info",
        alias="AUTH_SERVICE",
        env="AUTH_SERVICE",
    )

    backoff_max_retries: int = Field(
        5, alias="BACKOFF_MAX_RETRIES", env="BACKOFF_MAX_RETRIES"
    )

    batch_size: int = Field(250, alias="BATCH_SIZE", env="BATCH_SIZE")

    enable_tracer: bool = Field(False, alias="ENABLE_TRACER", env="ENABLE_TRACER")

    debug: bool = Field(True, alias="DEBUG", env="DEBUG")

    log_level: str = "INFO"
    logger_filename: str = "/opt/logs/file-api-logs.json"
    logger_maxbytes: int = 15000000
    logger_mod: str = "a"
    logger_backup_count: int = 5
    logger_rotation: str = Field("500 MB", alias="ROTATION", env="ROTATION")

    sentry_dsn: str | None = None

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()

ROUTING_KEYS = [
    settings.register_routing_key,
    settings.activating_routing_key,
    settings.long_no_see_routing_key,
    settings.message_routing_key,
    settings.bookmark_routing_key,
    settings.film_routing_key,
]


BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": (ClientConnectorError, RateLimitException),
    "logger": logger,
    "max_tries": settings.backoff_max_retries,
}


CIRCUIT_CONFIG = {"expected_exception": is_circuit_processable}
