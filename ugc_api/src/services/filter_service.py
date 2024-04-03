from datetime import datetime
from functools import lru_cache
from fastapi import Depends
from producers.abstract_producer import AbstractProducer
from models.filter import FilterEventDTO, FilterProduceEventDTO
from producers.kafka_producer import get_producer
from services.base_service import BaseService
from models.user import User


class SearchFilterSevice(BaseService):
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'messages'

    async def execute(self, search_filter: FilterEventDTO, user: User) -> FilterProduceEventDTO:

        search_filter = FilterProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.now(),
            **search_filter.model_dump(),
        )

        key = self._get_key(search_filter, include_fields=['user_id', 'genre_id', 'produce_timestamp',])
        message = self._get_message(search_filter)
        await self.producer.send(self.topic, key, message)

        return search_filter


@lru_cache
def get_search_filter_servece(
    producer: AbstractProducer = Depends(get_producer)
) -> SearchFilterSevice:
    return SearchFilterSevice(producer=producer)