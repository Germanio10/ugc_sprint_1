from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class WatchlistEventDTO(BaseModel):
    film_id: UUID

class WatchlistProduceEventDTO(WatchlistEventDTO):
    event_type: str = Field(default='watchlist')
    in_watchlist: bool
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)

class DeleteWatchlistEventDTO(WatchlistEventDTO):
    event_type: str = Field(default='watchlist_rm')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)