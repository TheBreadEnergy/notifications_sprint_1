from pydantic import BaseModel


class BaseEvent(BaseModel):
    user_id: str
