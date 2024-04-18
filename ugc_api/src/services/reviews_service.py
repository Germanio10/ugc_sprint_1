from datetime import datetime
from services.base_service import BaseService
from producers.abstract_producer import AbstractProducer, AbstractSortProducer

from models.reviews import ReviewsEventDTO, ReviewsProduceEventDTO, RatingInfoEventDTO, RatingInfoProduceEventDTO, ReviewsResposeDTO
from fastapi import Depends
from functools import lru_cache
from producers.kafka_producer import get_producer
from producers.mongo_producer import get_mongo_producer
from models.user import User


class AddToReviewsService(BaseService):

    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, review: ReviewsEventDTO, user: User) -> ReviewsProduceEventDTO:
        review = ReviewsProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.now(),
            **review.model_dump(),
        )
        key = self._get_key(review, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(review)
        await self.producer.send(self.topic, key, message)

        return review

class ReviewsRatingService(BaseService):
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, rating: RatingInfoEventDTO, user: User) -> RatingInfoProduceEventDTO:

        rating = RatingInfoProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.utcnow(),
            **rating.model_dump()
        )
        key = self._get_key(rating, include_fields=['user_id', 'review_id', 'produce_timestamp'])
        message = self._get_message(rating)
        await self.producer.send(self.topic, key, message)

        return rating

class GetReviewsService(BaseService):
    def __init__(self, producer: AbstractSortProducer) -> None:
        self.producer = producer
        self.collection = 'reviews'

    async def execute(self, user: User, field: str="review_timestamp", ascending: bool=True) -> list[ReviewsResposeDTO]:
        watchlist = await self.producer.get_sorted(self.collection, ReviewsResposeDTO, field, ascending)

        return watchlist
    
@lru_cache()
def add_to_reviews_service(
        producer: AbstractProducer = Depends(get_producer),
) -> AddToReviewsService:
    return AddToReviewsService(producer=producer)

@lru_cache()
def reviews_rating_service(
        producer: AbstractProducer = Depends(get_producer),
) -> ReviewsRatingService:
    return ReviewsRatingService(producer=producer)

@lru_cache()
def get_reviews_service(
        producer: AbstractSortProducer = Depends(get_mongo_producer),
) -> GetReviewsService:
    return GetReviewsService(producer=producer)
