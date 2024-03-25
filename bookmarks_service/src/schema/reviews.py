from pydantic import BaseModel
from src.schema.film import FilmMeta


class ReviewCreateDto(BaseModel):
    film: FilmMeta
    text: str


class ReviewUpdateDto(BaseModel):
    text: str
