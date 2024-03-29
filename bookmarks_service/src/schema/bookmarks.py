from datetime import datetime

from src.schema.film import FilmMeta
from src.schema.user import IdentifiableMixin


class BookmarkCreateDto(IdentifiableMixin):
    film: FilmMeta


class BookmarkDto(IdentifiableMixin):
    film: FilmMeta
    created: datetime
