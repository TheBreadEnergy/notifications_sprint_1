from pydantic import BaseModel
from src.schemas.base import IdentifiableMixin


class RoleBase(IdentifiableMixin):
    name: str
    description: str | None


class RoleDto(RoleBase):
    ...


class RoleCreateDto(BaseModel):
    name: str
    description: str | None


class RoleUpdateDto(RoleBase):
    name: str
    description: str | None


class Roles:
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"
