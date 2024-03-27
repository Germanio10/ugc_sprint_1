from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID


class BaseFilmProgressEvent(BaseModel):
    film_id: UUID
    watching_time: datetime = Field(...)
    film_percentage: int

    @classmethod
    def extract_minutes(cls, v):
        return v.minute


class FilmProgressEventDTO(BaseFilmProgressEvent):
    event_timestamp: datetime


class FilmProgressEventResponse(BaseFilmProgressEvent):
    pass
