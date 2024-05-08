import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    rabbit_login: str = Field("admin", alias="RABBIT_LOGIN", env="RABBIT_LOGIN")
    rabbit_password: str = Field(
        "password", alias="RABBIT_PASSWORD", env="RABBIT_PASSWORD"
    )
    grpc_port: int = Field(50051, alias="GRPC_PORT", env="GRPC_PORT")
    rabbit_host: str = Field("localhost", alias="RABBIT_HOST", env="RABBIT_HOST")
    rabbit_port: int = Field(5672, alias="RABBIT_PORT", env="RABBIT_PORT")
    queue_name: str = Field("workers", alias="QUEUE_NAME", env="QUEUE_NAME")
    delayed_exchange: str = Field(
        "workers-exchange", alias="DELAYED_EXCHANGE", env="DELAYED_EXCHANGE"
    )
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
        "workers.v1", alias="MESSAGE_VERSION", env="MESSAGE_VERSION"
    )

    auth_service: str = Field(
        "http://localhost:8001/api/v1/users/info",
        alias="AUTH_SERVICE",
        env="AUTH_SERVICE",
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
