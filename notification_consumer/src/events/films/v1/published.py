from pydantic import BaseModel


class FilmPublishedEvent(BaseModel):
    film_id: str
