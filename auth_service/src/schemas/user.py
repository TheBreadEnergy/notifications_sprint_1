import datetime
import uuid

from pydantic import BaseModel
from src.schemas.base import IdentifiableMixin
from src.schemas.role import RoleBase


class UserHistoryDto(IdentifiableMixin):
    user_id: uuid.UUID
    attempted: datetime.datetime
    user_agent: str
    success: bool


class UserBase(IdentifiableMixin):
    login: str
    email: str | None
    first_name: str | None
    last_name: str | None


class UserDto(UserBase):
    roles: list[RoleBase] | None


class UserCreateDto(BaseModel):
    login: str
    password: str
    first_name: str | None
    last_name: str | None
    email: str | None


class UserUpdateDto(BaseModel):
    login: str | None
    first_name: str | None
    last_name: str | None
    email: str | None


class UserUpdatePasswordDto(BaseModel):
    old_password: str
    new_password: str


class UserHistoryCreateDto(BaseModel):
    user_id: uuid.UUID
    attempted: datetime.datetime
    user_agent: str
    success: bool
