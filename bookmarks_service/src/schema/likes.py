from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel
from src.schema.film import FilmMeta
from src.schema.user import IdentifiableMixin, UserMeta


class LikeType(IntEnum):
    like = 0
    dislike = 1


class ReviewLikeMeta(BaseModel):
    type: LikeType
    user: UserMeta


class FilmLikeDto(IdentifiableMixin):
    film: FilmMeta
    user: UserMeta
    like_type: LikeType
    created: datetime


class FilmLikeCreateDto(BaseModel):
    film: FilmMeta
    like_type: LikeType
