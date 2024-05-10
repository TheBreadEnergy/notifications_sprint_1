from pydantic import BaseModel


class Status(BaseModel):
    code: str
    message: str
    description: list[str] = []
