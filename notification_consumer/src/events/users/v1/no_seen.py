from pydantic import BaseModel


class UserNotSeenEvent(BaseModel):
    user_id: str
