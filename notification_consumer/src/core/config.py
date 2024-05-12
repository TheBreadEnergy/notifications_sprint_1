from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix=".", env_file=".env")
    supported_versions: list[str] = ["v1"]
    user_registered_topic: str = Field(
        "user_registered", env="USER_REGISTERED_TOPIC", alias="USER_REGISTERED_TOPIC"
    )

    user_activated_topic: str = Field(
        "user_activated", env="USER_ACTIVATED_TOPIC", alias="USER_ACTIVATED_TOPIC"
    )

    user_no_see_topic: str = Field(
        "user_no_see", env="USER_NO_SEE_TOPIC", alias="USER_NO_SEE_TOPIC"
    )

    film_added_topic: str = Field(
        "film_added",
        env="FILM_ADDED_TOPIC",
        alias="FILM_ADDED_TOPIC",
    )
    kafka_host: str = Field("109.71.244.113", alias="KAFKA_HOST", env="KAFKA_HOST")

    kafka_port: int = Field(9094, alias="KAFKA_PORT", env="KAFKA_PORT")

    kafka_group: str = Field("messages", alias="KAFKA_GROUP", env="KAFKA_GROUP")

    notification_service: str = Field(
        "localhost:50051", env="NOTIFICATION_SERVICE", alias="NOTIFICATION_SERVICE"
    )


settings = Settings()


TOPICS = [
    f"{version}.{topic}"
    for topic in [
        settings.film_added_topic,
        settings.user_no_see_topic,
        settings.user_activated_topic,
        settings.user_registered_topic,
    ]
    for version in settings.supported_versions
]
