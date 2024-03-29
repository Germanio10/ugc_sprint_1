from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str


class FilterEventDTO(BaseModel):
    genre_id: UUID | None
    genre: str | None
    sort: str | None
    event_timestamp: datetime


class FilterProduceEventDTO(FilterEventDTO):
    user_id: str
    produce_timestamp: datetime
