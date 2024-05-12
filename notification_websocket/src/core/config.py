import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "Websocket notifications",
        alias="PROJECT_NAME",
        env="PROJECT_NAME",
    )
    description: str = Field(
        "Websocket уведомлений",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")

    debug: bool = Field(False, alias="DEBUG", env="DEBUG")

    # Logging settings
    log_level: str = "INFO"
    logger_filename: str = "/opt/logs/websockets-api-logs.json"
    logger_maxbytes: int = 15000000
    logger_mod: str = "a"
    logger_backup_count: int = 5

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
