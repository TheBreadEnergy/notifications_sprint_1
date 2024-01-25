from uuid import UUID

from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str
    description: str | None = None
