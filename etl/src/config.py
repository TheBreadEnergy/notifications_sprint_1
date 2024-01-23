import backoff
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.logger import logger


class PostgresDsn(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    dbname: str = Field(..., alias="POSTGRES_DB", env="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER", env="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD", env="POSTGRES_PASSWORD")
    host: str = Field(..., alias="POSTGRES_HOST", env="POSTGRES_HOST")
    port: str = Field(..., alias="POSTGRES_PORT", env="POSTGRES_PORT")


class ElasticDsn(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    host: str = Field(..., alias="ELASTICSEARCH_HOST", env="ELASTICSEARCH_HOST")
    port: str = Field(..., alias="ELASTICSEARCH_PORT", env="ELASTICSEARCH_PORT")


class RedisDsn(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    host: str = Field(..., alias="REDIS_HOST", env="REDIS_HOST")
    port: str = Field(..., alias="REDIS_PORT", env="REDIS_PORT")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    batch_size: int = Field(..., alias="BATCH_SIZE", env="BATCH_SIZE")
    scan_frequency: int = Field(..., alias="SCAN_FREQ", env="SCAN_FREQ")
    backoff_max_retries: int = (
        Field(..., alias="BACKOFF_MAX_RETRIES", env="BACKOFF_MAX_RETRIES"),
    )
    movie_index: str = Field(..., alias="MOVIE_INDEX", env="MOVIE_INDEX")
    movie_key: str = Field(..., alias="MOVIE_STATE_KEY", env="MOVIE_STATE_KEY")
    genre_index: str = Field(..., alias="GENRE_INDEX", env="GENRE_INDEX")
    genre_key: str = Field(..., alias="GENRE_STATE_KEY", env="GENRE_STATE_KEY")
    person_index: str = Field(..., alias="PERSON_INDEX", env="PERSON_INDEX")
    person_key: str = Field(..., alias="PERSON_STATE_KEY", env="PERSON_STATE_KEY")
    root_key: str = Field(..., alias="ROOT_STATE", env="ROOT_STATE")


POSTGRES_DSN = PostgresDsn()
ELASTIC_DSN = ElasticDsn()
REDIS_DSN = RedisDsn()
APP_SETTINGS = AppSettings()


BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "logger": logger,
    "max_tries": APP_SETTINGS.backoff_max_retries,
}
