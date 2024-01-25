from abc import ABC, abstractmethod
from uuid import UUID

from src.models.person import Person
from src.services.base import CachedRepositoryES, RepositoryES

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonRepositoryES(RepositoryES[Person]):
    def build_gets_query(self, *, sort: str, data_filter: dict) -> dict:
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
        return {"query": {"match_phrase_prefix": {"name": {"query": title}}}}


class CachedPersonRepository(CachedRepositoryES[Person]):
    ...


class PersonServiceABC(ABC):
    @abstractmethod
    def get(self, person_id: UUID) -> Person:
        ...

    @abstractmethod
    def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[Person]:
        ...

    @abstractmethod
    def search(self, *, name: str, page: int, size: int) -> list[Person]:
        ...


class PersonService(PersonServiceABC):
    def __init__(self, repository: RepositoryES[Person]):
        self._repository = repository

    async def get(self, person_id: UUID) -> Person:
        return await self._repository.get(entity_id=person_id)

    async def gets(
        self, *, sort: str, data_filter: dict, page: int, size: int
    ) -> list[Person]:
        return await self._repository.gets(
            sort=sort, data_filter=data_filter, page=page, size=size
        )

    async def search(self, *, name: str, page: int, size: int) -> list[Person]:
        return await self._repository.find(title=name, page=page, size=size)
