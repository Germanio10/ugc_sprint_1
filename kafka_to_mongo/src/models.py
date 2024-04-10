from datetime import datetime

from pydantic import BaseModel


class RatingEvent(BaseModel):
    film_id: str
    rating: int
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime
