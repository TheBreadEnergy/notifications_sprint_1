from pydantic import BaseModel


class UserRegisteredEvent(BaseModel):
    user_id: str
    short_url: str
