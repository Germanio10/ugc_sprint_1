from datetime import datetime
from functools import lru_cache

from fastapi import Depends

from producers.abstract_producer import AbstractProducer
from producers.kafka_producer import get_producer
from services.base_service import BaseService
from models.user import User
from models.rating import (RatingInfoEventDTO, RatingInfoProduceEventDTO, RatingDeleteInfoEventDTO,
                           RatingDeleteProduceEventDTO)


class RatingService(BaseService):
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, rating: RatingInfoEventDTO, user: User) -> RatingInfoProduceEventDTO:

        rating = RatingInfoProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.utcnow(),
            **rating.model_dump()
        )
        key = self._get_key(rating, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(rating)
        await self.producer.send(self.topic, key, message)

        return rating


class DeleteRatingService(BaseService):  ### Убрать дублирование
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, delete_rating: RatingDeleteInfoEventDTO, user: User) -> RatingDeleteProduceEventDTO:

        delete_rating = RatingDeleteProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.utcnow(),
            **delete_rating.model_dump()
        )
        key = self._get_key(delete_rating, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(delete_rating)
        await self.producer.send(self.topic, key, message)

        return delete_rating


@lru_cache()
def get_rating_service(
        producer: AbstractProducer = Depends(get_producer)
) -> RatingService:
    return RatingService(producer=producer)


@lru_cache()
def get_delete_rating_service(
        producer: AbstractProducer = Depends(get_producer)
) -> DeleteRatingService:
    return DeleteRatingService(producer=producer)