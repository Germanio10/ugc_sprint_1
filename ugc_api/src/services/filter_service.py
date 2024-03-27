from datetime import datetime
from functools import lru_cache
from fastapi import Depends, HTTPException
from producers.abstract_producer import AbstractProducer
from models.filter import FilterEventDTO, FilterProduceEventDTO
from producers.kafka_producer import get_producer
from services.base_service import BaseService
from clients.api_client import ApiClient, get_api_client
from core import exceptions
from models.user import User


class SearchFilterSevice(BaseService):
    def __init__(self, producer: AbstractProducer, api_client: ApiClient) -> None:
        self.producer = producer
        self.api_client = api_client
        self.topic = 'messages'

    async def execute(self, search_filter: FilterEventDTO, user: User) -> FilterProduceEventDTO:
        if search_filter.genre_id != None:
            path = f'/api/v1/genres/{search_filter.genre_id}/'

        try:
            genre = await self.api_client.get(path=path, cookies=user.cookies)
        except HTTPException:
            raise exceptions.GenreNotFoundError

        search_filter = FilterProduceEventDTO(
            user_id=user.user_id,
            genre=genre['name'],
            produce_timestamp=datetime.now(),
            **search_filter.model_dump(),
        )

        key = self._get_key(search_filter, exclude_fields=['produce_timestamp', ])
        message = self._get_message(search_filter)
        await self.producer.send(self.topic, key, message)

        return search_filter


@lru_cache
def get_search_filter_servece(
    producer: AbstractProducer = Depends(get_producer),
    api_client: ApiClient = Depends(get_api_client)
) -> SearchFilterSevice:
    return SearchFilterSevice(producer=producer, api_client=api_client)
