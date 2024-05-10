from pydantic import BaseModel


class UserActivatedEvent(BaseModel):
    user_id: str
