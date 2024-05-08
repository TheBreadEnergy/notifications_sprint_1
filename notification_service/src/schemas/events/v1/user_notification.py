from uuid import UUID

from pydantic import BaseModel


class UserNotificationSchema(BaseModel):
    task_id: UUID
    user_id: str


class UserLongNoSeeNotificationSchema(UserNotificationSchema):
    duration: int | None = None
