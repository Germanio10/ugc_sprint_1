from datetime import datetime

from pydantic import BaseModel


class FilmQualityEvent(BaseModel):
    film_id: str
    quality: int
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime


class ClickInfoEvent(BaseModel):
    url: str
    click_time: datetime
    time_on_page: int
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime


class FilmProgressEvent(BaseModel):
    film_id: str
    watching_time: int
    film_percentage: int
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime


class FilterEvent(BaseModel):
    genre_id: str | None
    genre: str | None
    sort: str | None
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime

class LikeEvent(BaseModel):
    film_id: str
    rating: int
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime


class RatingRmEvent(BaseModel):
    film_id: str
    event_timestamp: datetime
    user_id: str
    produce_timestamp: datetime

class WatchlistEvent(BaseModel):
    film_id: str
    in_watchlist: bool
    user_id: str
    produce_timestamp: datetime

class ReviewsEvent(BaseModel):
    film_id: str
    review: str
    name: str
    review_timestamp: datetime
    user_id: str
    produce_timestamp: datetime