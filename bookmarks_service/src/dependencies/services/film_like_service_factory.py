from functools import cache

from src.dependencies.registrator import add_factory_to_mapper
from src.repositories.film_likes import MongoFilmLikesRepository
from src.services.film_likes import FilmLikeService, FilmLikeServiceABC


@add_factory_to_mapper(FilmLikeServiceABC)
@cache
def create_film_like_service() -> FilmLikeService:
    return FilmLikeService(repo=MongoFilmLikesRepository())
