from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class Genre(BaseModel):
    id: UUID
    name: str


class FilmQualityEventDTO(BaseModel):
    film_id: UUID
    quality: int
    event_timestamp: datetime

    @validator('event_timestamp')
    def event_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)


class FilmQualityProduceEventDTO(FilmQualityEventDTO):
    event_type: str = Field(default='quality')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)

