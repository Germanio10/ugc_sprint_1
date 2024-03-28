from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str


class FilmQualityEventDTO(BaseModel):
    film_id: UUID
    film_title: str
    quality: int
    event_timestamp: datetime


class FilmQualityProduceEventDTO(FilmQualityEventDTO):
    user_id: str
    produce_timestamp: datetime

