import uuid
from uuid import UUID

from pydantic import BaseModel


class IdentifiableMixin(BaseModel):
    id: uuid.UUID


class RoleBase(IdentifiableMixin):
    name: str
    description: str | None


class UserMeta(BaseModel):
    user_id: UUID
    login: str | None
    email: str | None
    first_name: str | None
    last_name: str | None


class UserDto(IdentifiableMixin):
    login: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    roles: list[RoleBase] | None
