import datetime

from pydantic import BaseModel


class ShortUrlResponseSchema(BaseModel):
    url: str


class ShortLinkCreateSchema(BaseModel):
    url: str
    duration: int | None = None


class ShortDbLinkCreateSchema(BaseModel):
    short_link: str
    original_link: str
    expires_at: datetime.datetime
