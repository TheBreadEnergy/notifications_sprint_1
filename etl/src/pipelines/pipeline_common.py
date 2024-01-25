import time
from datetime import datetime
from typing import Generator, Tuple, Type, Union

import backoff
from src.common.coroutine import coroutine
from src.config import APP_SETTINGS, BACKOFF_CONFIG
from src.fetchers.base_fetcher import BaseFetcher
from src.loaders.base_loader import BaseLoader
from src.logger import logger
from src.models.genre_es import GenreES
from src.models.movie_es import MovieES
from src.models.person_es import PersonES
from src.state import State


def fetch_generator(query: str):
    @coroutine
    @backoff.on_exception(**BACKOFF_CONFIG)
    def fetch(fetcher: BaseFetcher, next_node: Generator) -> Generator[None, str, None]:
        while last_updated := (yield):
            logger.info(
                "Quering entities with modified date greater than %s, with query %s",
                last_updated,
                query,
            )
            for result in fetcher.fetch_many(
                query, APP_SETTINGS.batch_size, last_updated
            ):
                logger.info("Queried %s objects", len(result))
                next_node.send(result)

    return fetch


def transform_generator(
    entity_type: Union[Type[MovieES], Type[GenreES], Type[PersonES]]
):
    @coroutine
    def transform(next_node: Generator) -> Generator[None, list[dict], None]:
        while data := (yield):
            logger.info("Transformation step started")
            batch = []
            logger.info(data)
            for entity_dict in data:
                entity = entity_type(**entity_dict).model_dump()
                entity["_id"] = entity["id"]
                batch.append(entity)
            update_date = data[-1]["modified"]
            logger.info("Transformed %s records", len(data))
            next_node.send((batch, update_date))

    return transform


def save_generator(state_key: str):
    @coroutine
    @backoff.on_exception(**BACKOFF_CONFIG)
    def save(
        loader: BaseLoader, state: State
    ) -> Generator[None, Tuple[list[dict], datetime], None]:
        while movies := (yield):
            logger.info("Save state begins")
            t = time.perf_counter()
            logger.info(movies[0])
            lines = loader.load_batch(movies[0], APP_SETTINGS.batch_size)
            elapsed = time.perf_counter() - t
            if lines == 0:
                logger.info("Nothing to update in index")
            else:
                logger.info("%s lines was updated in %s", lines, elapsed)

            modified = movies[1]
            state.set_state(state_key, str(modified))
            logger.info("ES state was changed to %s date", modified)

    return save
