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

# class LikeReviewsEventDTO(BaseModel):
#     review_id: UUID

# class LikeReviewsProduceEventDTO(LikeReviewsEventDTO):
#     event_type: str = Field(default='like')
#     user_id: str
#     produce_timestamp: datetime

#     @validator('produce_timestamp')
#     def produce_timestamp_validate(cls, value: datetime):
#         return value.replace(tzinfo=None)
    
# class DeleteReviewsEventDTO(BaseModel):
#     film_id: UUID
#     event_type: str = Field(default='review_rm')
#     user_id: str
#     produce_timestamp: datetime

#     @validator('produce_timestamp')
#     def produce_timestamp_validate(cls, value: datetime):
#         return value.replace(tzinfo=None)
