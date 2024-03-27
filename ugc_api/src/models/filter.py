from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str


class FilterEventDTO(BaseModel):
    genre_id: UUID | None
    sort: str | None
    event_timestamp: datetime


class FilterProduceEventDTO(FilterEventDTO):
    user_id: str
    genre: str | None
    produce_timestamp: datetime


class FilterEventResponse(BaseModel):
    genre_id: UUID
