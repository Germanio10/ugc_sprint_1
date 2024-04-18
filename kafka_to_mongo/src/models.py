from datetime import datetime

from pydantic import BaseModel


class RatingEvent(BaseModel):
    film_id: str
    rating: int
    user_id: str


class WatchlistEvent(BaseModel):
    film_id: str
    in_watchlist: bool
    user_id: str


class ReviewsEvent(BaseModel):
    film_id: str
    review: str
    name: str
    review_timestamp: datetime
    user_id: str


class ReviewsRatingEvent(BaseModel):
    review_id: str
    rating: int
    user_id: str
