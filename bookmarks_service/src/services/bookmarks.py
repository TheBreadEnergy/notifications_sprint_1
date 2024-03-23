from abc import ABC, abstractmethod
from uuid import UUID

from src.core.pagination import PaginatedPage
from src.models.bookmark import Bookmark
from src.repositories.base import MongoRepository
from src.schema.bookmarks import BookmarkCreateDto
from src.schema.user import UserMeta


class BookmarkServiceABC(ABC):
    @abstractmethod
    async def get_bookmarks_for_user(self, user_id: UUID) -> PaginatedPage[Bookmark]:
        ...

    @abstractmethod
    async def create_bookmark(
        self, *, data: BookmarkCreateDto, user: UserMeta
    ) -> Bookmark:
        ...

    @abstractmethod
    async def delete_bookmark(self, bookmark_id: UUID) -> None:
        ...

    @abstractmethod
    async def delete_all_bookmarks_for_user(self, user_id: UUID) -> None:
        ...


class BookmarkService(BookmarkServiceABC):
    def __init__(self, repo: MongoRepository[Bookmark]):
        self._repo = repo

    async def create_bookmark(
        self, *, data: BookmarkCreateDto, user: UserMeta
    ) -> Bookmark:
        data = Bookmark(film=data.film, user=user)
        return await self._repo.insert(entity=data)

    async def delete_all_bookmarks_for_user(self, user_id: UUID) -> None:
        return await self._repo.delete(user_id=user_id)

    async def get_bookmarks_for_user(self, user_id: UUID) -> PaginatedPage[Bookmark]:
        return await self._repo.search(user_id=user_id)

    async def delete_bookmark(self, bookmark_id: UUID) -> None:
        return await self._repo.delete(entity_id=bookmark_id)
