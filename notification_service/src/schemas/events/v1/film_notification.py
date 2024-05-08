from uuid import UUID

from pydantic import BaseModel


class FilmNotificationSchema(BaseModel):
    task_id: UUID
    file_id: str
