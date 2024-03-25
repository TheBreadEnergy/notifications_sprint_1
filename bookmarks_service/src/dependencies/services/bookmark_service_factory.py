from functools import cache

from src.dependencies.registrator import add_factory_to_mapper
from src.repositories.bookmarks import MongoBookmarksRepository
from src.services.bookmarks import BookmarkService, BookmarkServiceABC


@add_factory_to_mapper(BookmarkServiceABC)
@cache
def create_bookmark_service() -> BookmarkService:
    return BookmarkService(repo=MongoBookmarksRepository())
