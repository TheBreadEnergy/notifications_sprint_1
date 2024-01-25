from uuid import UUID

from pydantic import BaseModel


class EntityMixinES(BaseModel):
    id: UUID
