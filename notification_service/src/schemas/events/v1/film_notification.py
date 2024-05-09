from pydantic import BaseModel


class FilmNotificationSchema(BaseModel):
    task_id: str
    file_id: str
