from uuid import UUID

from pydantic import BaseModel


class IdentifiableMixin(BaseModel):
    id: UUID
