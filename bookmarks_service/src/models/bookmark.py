from src.models.base import DomainBase


class Bookmark(DomainBase):
    class Settings:
        name = "bookmarks"
        use_state_management = True
