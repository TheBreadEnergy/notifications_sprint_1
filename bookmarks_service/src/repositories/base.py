from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar
from uuid import UUID

from fastapi_pagination.ext.beanie import paginate
from src.core.pagination import PaginatedPage
from src.models.base import DomainBase

ModelType = TypeVar("ModelType", bound=DomainBase)


class RepositoryABC(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def search(self, *args, **kwargs):
        ...

    @abstractmethod
    def insert(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...


class MongoRepository(RepositoryABC, Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def get(self, *, entity_id: UUID) -> ModelType:
        return await self._model.find_one(self._model.id == entity_id)

    async def search(
        self,
        *,
        user_id: UUID | None = None,
        film_id: UUID | None = None,
        sort_by: str | None = "created"
    ) -> PaginatedPage[ModelType]:
        if not user_id and not film_id:
            raise ValueError("You should provide either user_id or film_id")
        if user_id:
            query = self._model.find_many(self._model.user.user_id == user_id)
        else:
            query = self._model.find_many(self._model.film.film_id == film_id)
        if sort_by:
            query.sort(sort_by)
        return await paginate(query)

    async def insert(self, *, entity: ModelType):
        await entity.insert()
        return entity

    async def delete(
        self,
        *,
        entity_id: UUID | None = None,
        film_id: UUID | None = None,
        user_id: UUID | None = None
    ) -> None:
        if not entity_id and not film_id and not user_id:
            raise ValueError(
                "You should provide either entity_id or film_id or user_id"
            )
        if entity_id:
            query = self._model.find(self._model.id == entity_id)
        elif film_id:
            query = self._model.find(self._model.film_id == film_id)
        else:
            query = self._model.find(self._model.user.user_id == user_id)
        await query.delete()
