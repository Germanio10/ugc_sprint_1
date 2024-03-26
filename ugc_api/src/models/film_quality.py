from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str


class FilmQualityEventDTO(BaseModel):
    film_id: UUID
    quality: int
    event_timestamp: datetime


class FilmQualityProduceEventDTO(FilmQualityEventDTO):
    # user_id: UUID
    title: str
    imdb_rating: float | None
    genre: list[Genre] | None
    produce_timestamp: datetime


class FilmQualityEventResponse(BaseModel):
    film_id: UUID





    


