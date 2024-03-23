import uuid

from pydantic import BaseModel
from src.schema.film import FilmMeta


class BookmarkCreateDto(BaseModel):
    id: uuid.UUID
    film: FilmMeta
