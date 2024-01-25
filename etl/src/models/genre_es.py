from typing import Optional

from src.models.base import EntityMixinES


class GenreES(EntityMixinES):
    name: str
    description: Optional[str] = None
