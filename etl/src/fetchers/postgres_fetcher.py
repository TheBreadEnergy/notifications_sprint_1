from psycopg import Connection, ServerCursor
from src.config import APP_SETTINGS
from src.fetchers.base_fetcher import BaseFetcher


class PostgresFetcher(BaseFetcher):
    def __init__(self, pg_connection: Connection):
        self._pg_connection = pg_connection

    def fetch_many(
        self, query: str, size: int = APP_SETTINGS.batch_size, *args, **kwargs
    ):
        with ServerCursor(self._pg_connection, "fetcher") as cursor:
            cursor.execute(query, tuple(args))
            while items := cursor.fetchmany(size):
                yield items
