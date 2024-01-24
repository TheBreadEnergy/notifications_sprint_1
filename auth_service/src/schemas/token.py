from pydantic import BaseModel


class Token(BaseModel):
    access_token: str | None
    refresh_token: str | None


class TokenJti(BaseModel):
    access_token_jti: str | None
    refresh_token_jti: str | None
