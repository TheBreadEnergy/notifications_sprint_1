from src.models.bookmark import Bookmark
from src.repositories.base import MongoRepository


class MongoBookmarksRepository(MongoRepository[Bookmark]):
    def __init__(self):
        super().__init__(model=Bookmark)
