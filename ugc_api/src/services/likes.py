from datetime import datetime
from functools import lru_cache

from fastapi import Depends

from producers.abstract_producer import AbstractProducer
from producers.kafka_producer import get_producer
from services.base_service import BaseService
from models.user import User
from models.likes import LikeInfoEventDTO, LikeInfoProduceEventDTO


class LikeService(BaseService):
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'messages'

    async def execute(self, like: LikeInfoEventDTO, user: User) -> LikeInfoProduceEventDTO:

        like = LikeInfoProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.utcnow(),
            **like.model_dump()
        )
        key = self._get_key(like, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(like)
        await self.producer.send(self.topic, key, message)

        return like


@lru_cache()
def get_like_service(
        producer: AbstractProducer = Depends(get_producer)
) -> LikeService:
    return LikeService(producer=producer)
