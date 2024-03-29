import uuid

from pydantic import BaseModel


class Roles:
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"


class IdentifiableMixin(BaseModel):
    id: uuid.UUID


class RoleBase(IdentifiableMixin):
    name: str
    description: str | None


class UserMeta(IdentifiableMixin):
    login: str | None
    email: str | None
    first_name: str | None
    last_name: str | None


class UserDto(UserMeta):
    roles: list[RoleBase] | None
