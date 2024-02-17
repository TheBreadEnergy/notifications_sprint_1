import datetime
import uuid

from pydantic import BaseModel, EmailStr
from src.models.user import SocialNetworksEnum
from src.schemas.base import IdentifiableMixin
from src.schemas.role import RoleBase


class UserHistoryDto(IdentifiableMixin):
    user_id: uuid.UUID
    attempted: datetime.datetime
    user_agent: str
    user_device_type: str
    success: bool


class UserBase(IdentifiableMixin):
    login: str
    email: EmailStr | None
    first_name: str | None
    last_name: str | None


class UserDto(UserBase):
    roles: list[RoleBase] | None


class UserCreateDto(BaseModel):
    login: str
    password: str
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


class UserUpdateDto(BaseModel):
    login: str | None
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


class UserUpdatePasswordDto(BaseModel):
    old_password: str
    new_password: str


class UserHistoryCreateDto(BaseModel):
    user_id: uuid.UUID
    attempted: datetime.datetime
    user_agent: str
    user_device_type: str
    success: bool


class UserShortenedDto(BaseModel):
    user_id: uuid.UUID
    login: str | None
    email: str | None
    role: RoleBase


class SocialUser(BaseModel):
    id: str
    login: str
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    social_name: SocialNetworksEnum


class SocialCreateDto(BaseModel):
    user_id: uuid.UUID
    social_id: str
    social_name: SocialNetworksEnum
