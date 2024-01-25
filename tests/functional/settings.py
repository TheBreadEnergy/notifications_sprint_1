from faker import Faker
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Faker.seed(42)


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    es_host: str = Field("http://localhost:9200", alias="ELASTIC_HOST")
    es_movie_index: str = Field("movies", alias="ES_MOVIE_INDEX")
    es_genre_index: str = Field("genres", alias="ES_GENRE_INDEX")
    es_person_index: str = Field("persons", alias="ES_PERSON_INDEX")
    redis_host: str = Field("redis", alias="REDIS_HOST")
    redis_port: int = Field("6379", alias="REDIS_PORT")
    service_url: str = Field("http://localhost:81", alias="SERVICE_URL")


test_settings = TestSettings()
fake = Faker()
