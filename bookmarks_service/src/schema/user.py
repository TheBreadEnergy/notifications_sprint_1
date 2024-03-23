from uuid import UUID

from pydantic import BaseModel


class UserMeta(BaseModel):
    user_id: UUID
    login: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
