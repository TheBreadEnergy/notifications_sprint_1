import logging

from src.queries.base import BaseQuery
from src.queries.settings import MOVIE_TABLE, PERSON_MOVIE_TABLE, PERSON_TABLE

logger = logging.getLogger(__name__)


class PersonQuery(BaseQuery):
    _query = f"""
    SELECT person.id,
    person.full_name AS name,
    person.gender AS gender,
    COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('film_id', person_film.film_work_id, 'role', person_film.role)) FILTER (WHERE person_film.film_work_id IS NOT NULL), array[]::jsonb[]) AS film_roles,
    GREATEST (person.modified, MAX(film.modified)) as modified
    FROM {PERSON_TABLE} person
    LEFT JOIN {PERSON_MOVIE_TABLE} as person_film ON person.id = person_film.person_id
    LEFT JOIN {MOVIE_TABLE} as film ON person_film.film_work_id = film.id
    WHERE GREATEST (person.modified, film.modified) > %s
    GROUP BY person.id
    ORDER BY modified
    """

    def query(self):
        logger.info(self._query)
        return self._query
