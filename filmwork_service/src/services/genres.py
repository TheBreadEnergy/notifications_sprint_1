from abc import ABC, abstractmethod
from uuid import UUID

from src.models.genre import Genre
from src.services.base import CachedRepositoryES, RepositoryES

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreRepository(RepositoryES[Genre]):
    def build_gets_query(self, *, sort: str, data_filter: dict) -> dict:
        if not sort:
            sort = "asc"
        query = {
            "query": {"bool": {"filter": {"bool": {"must": []}}}},
            "sort": [{"name.raw": {"order": sort}}],
        }
        if "id" in data_filter:
            query["query"]["bool"]["filter"]["bool"]["must"].append(
                {"term": {"_id": data_filter["id"]}}
            )
        return query

    def build_find_query(self, title: str) -> dict:
        query = {"query": {"match_phrase_prefix": {"name": {"query": title}}}}
        return query


class CachedGenreRepository(CachedRepositoryES[Genre]):
    ...


class GenreServiceABC(ABC):
    @abstractmethod
    def get(self, genre_id: UUID) -> Genre:
        ...

    @abstractmethod
    def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[Genre]:
        ...

    @abstractmethod
    def search(self, *, name: str, page: int, size: int) -> list[Genre]:
        ...


class GenreService(GenreServiceABC):
    def __init__(self, repository: RepositoryES[Genre]):
        self._repository = repository

    async def get(self, genre_id: UUID) -> Genre:
        return await self._repository.get(entity_id=genre_id)

    async def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[Genre]:
        return await self._repository.gets(
            sort=sort, data_filter=data_filter, page=page, size=size
        )

    async def search(self, *, name: str, page: int, size: int):
        return await self._repository.find(title=name, page=page, size=size)
