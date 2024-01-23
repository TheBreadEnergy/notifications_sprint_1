from pydantic import BaseModel


class UserLoginDto(BaseModel):
    login: str
    password: str


class RefreshRequestDto(BaseModel):
    jti: str | None
