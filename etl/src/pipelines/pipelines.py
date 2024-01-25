from datetime import datetime
from typing import Generator, Type, Union

from src.fetchers.base_fetcher import BaseFetcher
from src.loaders.base_loader import BaseLoader
from src.logger import logger
from src.models.genre_es import GenreES
from src.models.movie_es import MovieES
from src.models.person_es import PersonES
from src.state import State

from .pipeline_common import fetch_generator, save_generator, transform_generator


def build_pipeline(
    pg_fetcher: BaseFetcher,
    state: State,
    es_loader: BaseLoader,
    query: str,
    redis_key: str,
    entity_type: Union[Type[MovieES], Type[GenreES], Type[PersonES]],
):
    saver_gen = save_generator(redis_key)
    transformer_gen = transform_generator(entity_type)
    fetcher_gen = fetch_generator(query)
    saver_coro = saver_gen(es_loader, state)
    transformer_coro = transformer_gen(next_node=saver_coro)
    fetcher_coro = fetcher_gen(pg_fetcher, next_node=transformer_coro)
    return fetcher_coro


def start_pipeline(state: State, key: str, pipeline: Generator):
    last_update = state.get_state(key) or str(datetime.min)
    logger.info("==== Last update in %s index was %s", key, last_update)
    pipeline.send(last_update)
