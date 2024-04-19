from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator


class FilmProgressEventDTO(BaseModel):
    film_id: UUID
    watching_time: int
    film_percentage: int
    event_timestamp: datetime

    @validator('event_timestamp')
    def event_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)


class FilmProgressProduceEventDTO(FilmProgressEventDTO):
    event_type: str = Field(default='progress')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)
