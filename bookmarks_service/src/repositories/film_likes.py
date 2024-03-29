from src.models.film_like import FilmLike
from src.repositories.base import MongoRepository


class MongoFilmLikesRepository(MongoRepository[FilmLike]):
    def __init__(self):
        super().__init__(model=FilmLike)
