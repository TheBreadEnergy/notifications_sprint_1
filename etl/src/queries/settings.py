from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")


class DatabaseSettings(EnvironmentBaseSettings):
    database_schema: str = Field("content", alias="DB_SCHEMA", env="DB_SCHEMA")
    database_movie_table: str = Field(
        "film_work", alias="DB_MOVIE_TABLE", env="DB_MOVIE_TABLE"
    )
    database_genre_table: str = Field(
        "genre", alias="DB_GENRE_TABLE", env="DB_GENRE_TABLE"
    )
    database_person_table: str = Field(
        "person", alias="DB_PERSON_TABLE", env="DB_PERSON_TABLE"
    )
    database_movie_genre_m2m_table: str = Field(
        "genre_film_work",
        alias="DB_MOVIE_GENRE_M2M_TABLE",
        env="DB_MOVIE_GENRE_M2M_TABLE",
    )
    database_movie_person_m2m_table: str = Field(
        "person_film_work", alias="DB_MOVIE_PERSON_M2M_TABLE"
    )


DB_SETTINGS = DatabaseSettings()


MOVIE_TABLE = f"{DB_SETTINGS.database_schema}.{DB_SETTINGS.database_movie_table}"

PERSON_TABLE = f"{DB_SETTINGS.database_schema}.{DB_SETTINGS.database_person_table}"

PERSON_MOVIE_TABLE = (
    f"{DB_SETTINGS.database_schema}.{DB_SETTINGS.database_movie_person_m2m_table}"
)

GENRE_TABLE = f"{DB_SETTINGS.database_schema}.{DB_SETTINGS.database_genre_table}"

GENRE_MOVIE_TABLE = (
    f"{DB_SETTINGS.database_schema}.{DB_SETTINGS.database_movie_genre_m2m_table}"
)
