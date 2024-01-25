import time
from contextlib import closing

import backoff
import psycopg
from elasticsearch import Elasticsearch
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from redis import Redis
from src.config import (
    APP_SETTINGS,
    BACKOFF_CONFIG,
    ELASTIC_DSN,
    POSTGRES_DSN,
    REDIS_DSN,
)
from src.fetchers.postgres_fetcher import PostgresFetcher
from src.loaders.elastic_loader import ElasticLoader
from src.logger import logger
from src.models.genre_es import GenreES
from src.models.movie_es import MovieES
from src.models.person_es import PersonES
from src.pipelines.pipelines import build_pipeline, start_pipeline
from src.queries.genre import GenreQuery
from src.queries.movie import MovieQuery
from src.queries.person import PersonQuery
from src.state import State
from src.storage.redis_storage import RedisStorage


@backoff.on_exception(**BACKOFF_CONFIG)
def main() -> None:
    postgres_dsn = make_conninfo(**POSTGRES_DSN.model_dump())
    elastic_dsn = f"http://{ELASTIC_DSN.host}:{ELASTIC_DSN.port}"
    print(elastic_dsn)
    redis_client = Redis(**REDIS_DSN.model_dump())
    state = State(
        RedisStorage(
            redis_adapter=redis_client, logger=logger, name=APP_SETTINGS.root_key
        )
    )

    with closing(
        psycopg.connect(postgres_dsn, row_factory=dict_row)
    ) as connection, closing(Elasticsearch([elastic_dsn], timeout=60)) as es_client:
        pg_fetcher = PostgresFetcher(pg_connection=connection)
        movie_pipeline = build_pipeline(
            pg_fetcher=pg_fetcher,
            state=state,
            es_loader=ElasticLoader(es_client, APP_SETTINGS.movie_index),
            query=MovieQuery().query(),
            redis_key=APP_SETTINGS.movie_key,
            entity_type=MovieES,
        )
        genre_pipeline = build_pipeline(
            pg_fetcher=pg_fetcher,
            state=state,
            es_loader=ElasticLoader(es_client, APP_SETTINGS.genre_index),
            query=GenreQuery().query(),
            redis_key=APP_SETTINGS.genre_key,
            entity_type=GenreES,
        )
        person_pipeline = build_pipeline(
            pg_fetcher=pg_fetcher,
            state=state,
            es_loader=ElasticLoader(es_client, APP_SETTINGS.person_index),
            query=PersonQuery().query(),
            redis_key=APP_SETTINGS.person_key,
            entity_type=PersonES,
        )
        pipelines = {
            APP_SETTINGS.movie_key: movie_pipeline,
            APP_SETTINGS.genre_key: genre_pipeline,
            APP_SETTINGS.person_key: person_pipeline,
        }
        while True:
            for key, pipeline in pipelines.items():
                start_pipeline(state=state, key=key, pipeline=pipeline)
            time.sleep(APP_SETTINGS.scan_frequency)


if __name__ == "__main__":
    main()
