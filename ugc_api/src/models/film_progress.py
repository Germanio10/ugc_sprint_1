from datetime import datetime

from pydantic import BaseModel
from uuid import UUID

from models.film_quality import Genre


class FilmProgressEventDTO(BaseModel):
    film_id: UUID
    watching_time: str
    film_percentage: int
    event_timestamp: datetime


class FilmProgressProduceEventDTO(FilmProgressEventDTO):
    user_id: str
    title: str
    imdb_rating: float | None
    genre: list[Genre] | None
    produce_timestamp: datetime


class FilmProgressEventResponse(BaseModel):
    film_id: UUID
