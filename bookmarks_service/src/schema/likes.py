from enum import IntEnum

from pydantic import BaseModel
from src.schema.user import UserMeta


class LikeType(IntEnum):
    like = 0
    dislike = 1


class ReviewLikeMeta(BaseModel):
    type: LikeType
    user: UserMeta
