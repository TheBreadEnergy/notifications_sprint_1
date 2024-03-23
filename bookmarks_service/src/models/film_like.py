from src.models.base import DomainBase
from src.schema.likes import LikeType


class FilmLike(DomainBase):
    like_type: LikeType

    class Settings:
        use_cache = True
        name = "likes"
        use_state_management = True
