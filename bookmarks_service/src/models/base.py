import datetime
import uuid

from beanie import Document
from pydantic import BaseModel, Field
from src.schema.film import FilmMeta
from src.schema.user import UserMeta


class IdentifiableMixin(BaseModel):
    id: uuid.UUID


class DomainBase(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    film: FilmMeta
    user: UserMeta
    created: datetime.datetime = Field(default=datetime.datetime.now(datetime.UTC))
