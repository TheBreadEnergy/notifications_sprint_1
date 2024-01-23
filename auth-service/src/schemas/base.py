import uuid

from pydantic import BaseModel


class IdentifiableMixin(BaseModel):
    id: uuid.UUID
