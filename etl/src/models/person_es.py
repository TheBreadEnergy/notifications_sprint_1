from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from src.models.base import EntityMixinES


class PersonFilmworkRoleES(BaseModel):
    film_id: UUID
    role: str


class PersonES(EntityMixinES):
    name: str
    gender: Optional[str] = ""
    film_roles: Optional[List[PersonFilmworkRoleES]] = []
