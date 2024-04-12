from datetime import datetime
from services.base_service import BaseService
from producers.abstract_producer import AbstractProducer

from models.reviews import ReviewsEventDTO, ReviewsProduceEventDTO
from fastapi import Depends
from functools import lru_cache
from producers.kafka_producer import get_producer
from models.user import User


class AddToReviewsService(BaseService):

    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'messages'

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

# class LikeReviewsService(BaseService):

#     def __init__(self, producer: AbstractProducer) -> None:
#         self.producer = producer
#         self.topic = 'messages'

#     async def execute(self, review: DeleteReviewsEventDTO, user: User) -> DeleteReviewsEventDTO:
#         review = DeleteReviewsEventDTO(
#             user_id=user.user_id,
#             produce_timestamp=datetime.now(),
#             **review.model_dump(),
#         )
#         key = self._get_key(review, include_fields=['user_id', 'film_id', 'produce_timestamp'])
#         message = self._get_message(review)
#         await self.producer.send(self.topic, key, message)

#         return review


@lru_cache()
def add_to_reviews_service(
        producer: AbstractProducer = Depends(get_producer),
) -> AddToReviewsService:
    return AddToReviewsService(producer=producer)

# @lru_cache()
# def remove_from_reviews_service(
#         producer: AbstractProducer = Depends(get_producer),
# ) -> LikeReviewsService:
#     return LikeReviewsService(producer=producer)
