from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class FilmProgressEventDTO(BaseModel):
    film_id: UUID
    watching_time: str
    film_percentage: int
    event_timestamp: datetime


class FilmProgressProduceEventDTO(FilmProgressEventDTO):
    user_id: str
    produce_timestamp: datetime


class FilmProgressEventResponse(BaseModel):
    message: str
