from abc import ABC, abstractmethod
from uuid import UUID

from src.models.film import Film
from src.services.base import CachedRepositoryES, RepositoryES

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


def build_sort(sort: str) -> list[dict]:
    sort_fields = []
    if sort:
        direction_sort = "asc"
        if sort.startswith("-"):
            direction_sort = "desc"
            sort = sort[1:]
        if sort == "title":
            sort_fields.append({"title.raw": direction_sort})
        elif sort == "imdb_rating":
            sort_fields.append({sort: direction_sort})
    return sort_fields


def build_filter(data_filter: dict) -> list[dict]:
    filters = []
    for f_item in data_filter:
        item = f_item.lower()
        if item in ["actors", "writers", "genres"]:
            filters.append(
                {
                    "nested": {
                        "path": f_item,
                        "query": {"term": {f"{f_item}.id": data_filter[f_item]}},
                    }
                }
            )
    return filters


class FilmRepository(RepositoryES[Film]):
    def build_find_query(self, title: str) -> dict:
        return {"query": {"match_phrase_prefix": {"title": {"query": title}}}}

    def build_gets_query(self, *, sort: str, data_filter: dict) -> dict:
        query = {
            "query": {"bool": {"must": build_filter(data_filter)}},
            "sort": build_sort(sort),
        }
        return query


class CachedFilmRepository(CachedRepositoryES[Film]):
    ...


class FilmServiceABC(ABC):
    @abstractmethod
    def get(self, film_id: UUID) -> Film | None:
        ...

    @abstractmethod
    def gets(self, *, sort: str, data_filter: dict, page: int, size: int) -> list[Film]:
        ...

    @abstractmethod
    def search(self, *, title: str, page: int, size: int) -> list[Film]:
        ...


class FilmService(FilmServiceABC):
    def __init__(self, repository: RepositoryES[Film]):
        self._repository = repository

    async def get(self, entity_id: UUID) -> Film | None:
        return await self._repository.get(entity_id=entity_id)

    async def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[Film]:
        return await self._repository.gets(
            sort=sort, data_filter=data_filter, page=page, size=size
        )

    async def search(self, *, title: str, page: int, size: int) -> list[Film]:
        return await self._repository.find(title=title, page=page, size=size)
