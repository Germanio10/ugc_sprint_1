from datetime import datetime
from functools import lru_cache

from core.config import settings
from fastapi import Depends, HTTPException, status
from models.rating import (
    AverageRating,
    RatingDeleteInfoEventDTO,
    RatingDeleteProduceEventDTO,
    RatingInfoEventDTO,
    RatingInfoProduceEventDTO,
)
from models.user import User
from producers.abstract_producer import AbstractProducer
from producers.kafka_producer import get_producer
from pymongo import MongoClient
from services.base_service import BaseService


class RatingService(BaseService):
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, rating: RatingInfoEventDTO, user: User) -> RatingInfoProduceEventDTO:

        rating = RatingInfoProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.utcnow(),
            **rating.model_dump(),
        )
        key = self._get_key(rating, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(rating)
        await self.producer.send(self.topic, key, message)

        return rating


class DeleteRatingService(BaseService):  ### Убрать дублирование
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(
        self,
        delete_rating: RatingDeleteInfoEventDTO,
        user: User,
    ) -> RatingDeleteProduceEventDTO:

        delete_rating = RatingDeleteProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.utcnow(),
            **delete_rating.model_dump(),
        )
        key = self._get_key(
            delete_rating,
            include_fields=['user_id', 'film_id', 'produce_timestamp'],
        )
        message = self._get_message(delete_rating)
        await self.producer.send(self.topic, key, message)

        return delete_rating


class AverageRatingService(BaseService):

    def __init__(self) -> None:
        self.client = MongoClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        self.collection = 'rating_info'

    async def get_average_rating(self, film_id, user: User):
        db = self.client['UGC']
        collection = db[self.collection]

        document = collection.find_one({'film_id': film_id})
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='У этого фильма нет оценок',
            )
        average_rating = document['average_rating']
        return AverageRating(average_rating=average_rating)


@lru_cache()
def get_rating_service(producer: AbstractProducer = Depends(get_producer)) -> RatingService:
    return RatingService(producer=producer)


@lru_cache()
def get_delete_rating_service(
    producer: AbstractProducer = Depends(get_producer),
) -> DeleteRatingService:
    return DeleteRatingService(producer=producer)


@lru_cache()
def get_average_rating_service() -> AverageRatingService:
    return AverageRatingService()
