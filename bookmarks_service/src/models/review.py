from pydantic import Field
from src.models.base import DomainBase
from src.schema.likes import ReviewLikeMeta


class Review(DomainBase):
    text: str
    likes: list[ReviewLikeMeta] = Field(default=list())

    class Settings:
        use_cache = True
        name = "reviews"
        use_state_management = True
