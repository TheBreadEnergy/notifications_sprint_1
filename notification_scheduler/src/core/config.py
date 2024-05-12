import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")

    project_name: str = "Notifications scheduler"

    description: str = "Планировщик повторяющихся уведомлений"

    postgres_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://app:123qwe@localhost:5432/notify_database",
        alias="POSTGRES_DNS",
        env="POSTGRES_DSN",
    )

    interval: int = Field(250, alias="INTERVAL", env="INTERVAL")

    db_schema: str = Field("content", alias="DB_SCHEMA", env="DB_SCHEMA")

    notifications_grpc: str = Field(
        "localhost:50051", alias="NOTIFICATIONS_GRPC", env="NOTIFICATIONS_GRPC"
    )

    debug: bool = Field(False, alias="DEBUG", env="DEBUG")

    delta: int = Field(300, alias="DELTA", env="DELTA")

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
