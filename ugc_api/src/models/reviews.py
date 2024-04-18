from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class ReviewsEventDTO(BaseModel):
    film_id: UUID
    review: str
    name: str
    review_timestamp: datetime

    @validator('review_timestamp')
    def event_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)

class ReviewsProduceEventDTO(ReviewsEventDTO):
    event_type: str = Field(default='reviews')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)
    
class RatingInfoEventDTO(BaseModel):
    review_id: UUID
    rating: int

class RatingInfoProduceEventDTO(RatingInfoEventDTO):
    event_type: str = Field(default='reviews_rating')
    user_id: str
    produce_timestamp: datetime

    @validator('produce_timestamp')
    def produce_timestamp_validate(cls, value: datetime):
        return value.replace(tzinfo=None)

class ReviewsResposeDTO(BaseModel):
    _id: str
    film_id: UUID
    review: str
    name: str
    review_timestamp: datetime
    user_id: str