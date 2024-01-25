from typing import List, Optional

from src.models.base import EntityMixinES


class FilmParticipantES(EntityMixinES):
    name: str


class FilmGenreES(EntityMixinES):
    name: str


class MovieES(EntityMixinES):
    title: str
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = []
    file: str | None = ""
    description: Optional[str] = None
    director: Optional[List[str]] = []
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
    actors: Optional[List[FilmParticipantES]] = []
    writers: Optional[List[FilmParticipantES]] = []
    genres: Optional[List[FilmGenreES]] = []
