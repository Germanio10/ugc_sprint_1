from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator


class Genre(BaseModel):
    id: UUID
    name: str


class FilterEventDTO(BaseModel):
    genre_id: UUID | None
    genre: str | None
    sort: str | None
    event_timestamp: datetime

    @validator('event_timestamp')
    def event_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)


class FilterProduceEventDTO(FilterEventDTO):
    event_type: str = Field(default='filter')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)
