import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field(
        "ETL Kafka в ClickHouse", alias="PROJECT_NAME", env="PROJECT_NAME"
    )
    description: str = Field(
        "Загрузка данных из Kafka в ClickHouse",
        alias="DESCRIPTION",
        env="DESCRIPTION",
    )

    CH_HOST: str = Field("localhost", alias="CH_HOST", env="CH_HOST")
    CH_PORT: int = Field(9000, alias="CH_PORT", env="CH_PORT")

    KAFKA_CLICK_TOPIC: str = Field(
        "clicks", alias="KAFKA_CLICK_TOPIC", env="KAFKA_CLICK_TOPIC"
    )
    KAFKA_SEEN_TOPIC: str = Field(
        "seens", alias="KAFKA_SEEN_TOPIC", env="KAFKA_SEEN_TOPIC"
    )
    KAFKA_VIDEO_TOPIC: str = Field(
        "video_qualities", alias="KAFKA_VIDEO_TOPIC", env="KAFKA_VIDEO_TOPIC"
    )
    KAFKA_FILM_TOPIC: str = Field(
        "film_views", alias="KAFKA_FILM_TOPIC", env="KAFKA_FILM_TOPIC"
    )
    KAFKA_FILTER_TOPIC: str = Field(
        "filters", alias="KAFKA_FILTER_TOPIC", env="KAFKA_FILTER_TOPIC"
    )
    KAFKA_HOST: str = Field("localhost", alias="KAFKA_HOST", env="KAFKA_HOST")
    KAFKA_PORT: int = Field(9094, alias="KAFKA_PORT", env="KAFKA_PORT")
    KAFKA_GROUP: str = Field("movies", alias="KAFKA_PORT", env="KAFKA_GROUP")

    base_dir: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
