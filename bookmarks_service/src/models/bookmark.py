from src.models.base import DomainBase


class Bookmark(DomainBase):
    class Settings:
        use_cache = True
        name = "bookmarks"
        use_state_management = True
