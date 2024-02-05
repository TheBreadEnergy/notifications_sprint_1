from pydantic import BaseModel


class TokenValidation(BaseModel):
    access_token: str
