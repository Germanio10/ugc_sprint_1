from datetime import datetime

from pydantic import BaseModel


class RatingEvent(BaseModel):
    film_id: str
    rating: int
    user_id: str
