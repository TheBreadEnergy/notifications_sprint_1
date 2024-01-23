from src.queries.base import BaseQuery
from src.queries.settings import GENRE_TABLE


class GenreQuery(BaseQuery):
    _query = f"""
    SELECT genre.id as id, 
    genre.name, genre.description as description,
    genre.modified as modified
    FROM {GENRE_TABLE} genre
    WHERE genre.modified > %s
    GROUP BY genre.id
    ORDER BY modified
    """

    def query(self):
        return self._query
