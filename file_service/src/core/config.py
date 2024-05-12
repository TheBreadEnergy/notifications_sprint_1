import os.path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "API для загрузки и хранения файлов", alias="PROJECT_NAME", env="PROJECT_NAME"
    )
    description: str = Field(
        "Загрузка, хранение и выдача информации и файлов,"
        " хранимых в файловом хранилище",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )
    version: str = Field("1.0.0", alias="VERSION", env="VERSION")
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST", env="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT", env="REDIS_PORT")
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    postgres_conn: PostgresDsn = Field(
        "postgresql+psycopg://app:123qwe@localhost:5432/movie_database",
        alias="POSTGRES_CONN",
        env="POSTGRES_CONN",
    )
    s3_bucket: str = Field("movies", alias="S3_BUCKET", env="S3_BUCKET")
    endpoint: str = Field(
        "localhost:9000", alias="MINIO_ENDPOINT", env="MINIO_ENDPOINT"
    )
    access_key: str = Field(
        "slGmrA9lbv0TKyGtqU4I", alias="MINIO_ACCESS_KEY", env="MINIO_ACCESS_KEY"
    )
    secret_key: str = Field(
        "4sjc7xUdS4543TSFqPn7famG6I4c0mUjGnlMJtHW",
        alias="MINIO_SECRET_KEY",
        env="MINIO_SECRET_KEY",
    )

    # Logging settings
    log_level: str = "INFO"
    logger_filename: str = "/opt/logs/file-api-logs.json"
    logger_maxbytes: int = 15000000
    logger_mod: str = "a"
    logger_backup_count: int = 5

    sentry_dsn: str | None = None

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
