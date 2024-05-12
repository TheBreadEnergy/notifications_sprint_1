import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")

    project_name: str = "Notifications scheduler"
    description: str = "Планировщик повторяющихся уведомлений"

    app_port: int = 8000
    debug: bool = False

    postgres_dsn: PostgresDsn = "postgresql+asyncpg://app:123qwe@localhost:5432/notify_database"
    db_schema: str = "content"

    notifications_grpc: str = "notifications-grpc:50051"

    debug: bool = Field(False, alias="DEBUG", env="DEBUG")

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
