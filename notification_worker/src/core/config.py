import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "Worker notifications",
        alias="PROJECT_NAME",
        env="PROJECT_NAME",
    )
    description: str = Field(
        "Worker уведомлений",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    postgres_conn: PostgresDsn = Field(
        "postgresql+asyncpg://app:123qwe@localhost:5432/notify_database",
        alias="DATABASE_CONN",
        env="DATABASE_CONN",
    )
    db_schema: str = Field("content", alias="DB_SCHEMA", env="DB_SCHEMA")
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    rabbit_login: str = Field("admin", alias="RABBIT_LOGIN", env="RABBIT_LOGIN")
    rabbit_password: str = Field(
        "password", alias="RABBIT_PASSWORD", env="RABBIT_PASSWORD"
    )
    rabbit_host: str = Field("localhost", alias="RABBIT_HOST", env="RABBIT_HOST")
    rabbit_port: int = Field(5672, alias="RABBIT_PORT", env="RABBIT_PORT")
    queue_name: str = Field("workers", alias="QUEUE_NAME", env="QUEUE_NAME")

    retry_exchange: str = Field("workers-exchange-retry", alias="RETRY_EXCHANGE")
    sorting_exchange: str = Field(
        "workers-exchange-sorting", alias="SORTING_EXCHANGE", env="SORTING_EXCHANGE"
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
    welcome_template_name: str = Field(
        "welcome_template", alias="WELCOME_TEMPLATE_NAME", env="WELCOME_TEMPLATE_NAME"
    )
    routing_prefix: str = Field(
        "workers", alias="MESSAGE_VERSION", env="MESSAGE_VERSION"
    )
    supported_message_versions: list[str] = ["v1"]

    host_email: str = Field(
        "your-email@example.com", alias="HOST_EMAIL", env="HOST_EMAIL"
    )
    sendgrid_api_key: str = Field(
        "key", alias="SENDGRID_API_KEY", env="SENDGRID_API_KEY"
    )

    debug: bool = Field(False, alias="DEBUG", env="DEBUG")

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
