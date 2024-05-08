from pydantic import BaseModel


class UserNotificationSchema(BaseModel):
    task_id: str | None
    user_id: str


class UserLongNoSeeNotificationSchema(UserNotificationSchema):
    duration: int | None = None
