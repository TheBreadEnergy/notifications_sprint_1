from pydantic import BaseModel


class StatusSchema(BaseModel):
    status: int
    message: str
    description: list[str]
