from abc import ABC, abstractmethod
from uuid import UUID

from src.core.pagination import PaginatedPage
from src.models.film_like import FilmLike
from src.repositories.base import MongoRepository
from src.schema.film import FilmMeta
from src.schema.likes import LikeType
from src.schema.user import UserMeta


class FilmLikeServiceABC(ABC):
    @abstractmethod
    async def get_film_likes(
        self, film_id: UUID | None = None, user_id: UUID | None = None
    ) -> PaginatedPage[FilmLike]:
        ...

    @abstractmethod
    async def create_film_like(
        self, film_id: UUID, user: UserMeta, like_type: LikeType
    ) -> FilmLike:
        ...

    @abstractmethod
    async def delete_film_like(self, film_id: UUID, user_id: UUID) -> None:
        ...


class FilmLikeService(FilmLikeServiceABC):
    def __init__(self, repo: MongoRepository[FilmLike]):
        self._repository = repo

    async def get_film_likes(
        self, film_id: UUID | None = None, user_id: UUID | None = None
    ) -> PaginatedPage[FilmLike]:
        return await self._repository.search(film_id=film_id, user_id=user_id)

    async def create_film_like(
        self, film: FilmMeta, user: UserMeta, like_type: LikeType
    ) -> FilmLike:
        film_like = FilmLike(film=film, user=user, like_type=like_type)
        return await self._repository.insert(entity=film_like)

    async def delete_film_like(self, film_id: UUID, user_id: UUID) -> None:
        return await self._repository.delete(film_id=film_id, user_id=user_id)
