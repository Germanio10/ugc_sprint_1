from datetime import datetime
from pydantic import BaseModel, Field, validator
from uuid import UUID


class LikeInfoEventDTO(BaseModel):
    film_id: UUID
    rating: int
    event_timestamp: datetime

    @validator('event_timestamp')
    def event_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)


class LikeInfoProduceEventDTO(LikeInfoEventDTO):
    event_type: str = Field(default='like')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)
