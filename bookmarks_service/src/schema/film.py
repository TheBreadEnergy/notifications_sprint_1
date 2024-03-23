from uuid import UUID

from pydantic import BaseModel


class FilmMeta(BaseModel):
    film_id: UUID
    name: str
    description: str
    genres: list[str]
