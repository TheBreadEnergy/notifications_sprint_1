from pydantic import BaseModel
from src.schema.film import FilmMeta
from src.schema.likes import LikeType, ReviewLikeMeta
from src.schema.user import IdentifiableMixin


class ReviewCreateDto(BaseModel):
    film: FilmMeta
    text: str


class ReviewUpdateDto(BaseModel):
    text: str


class ReviewDto(IdentifiableMixin):
    film: FilmMeta
    text: str
    likes: list[ReviewLikeMeta]


class ReviewLikeCreateDto(BaseModel):
    like_type: LikeType
