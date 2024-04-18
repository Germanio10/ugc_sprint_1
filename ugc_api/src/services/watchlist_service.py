from datetime import datetime
from services.base_service import BaseService
from producers.abstract_producer import AbstractProducer, AbstractSortProducer
from producers.mongo_producer import get_mongo_producer

from models.watchlist import WatchlistEventDTO, WatchlistProduceEventDTO, DeleteWatchlistEventDTO
from fastapi import Depends
from functools import lru_cache
from producers.kafka_producer import get_producer
from models.user import User


class AddToWatchlistService(BaseService):

    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, watchlist: WatchlistEventDTO, user: User) -> WatchlistProduceEventDTO:
        watchlist = WatchlistProduceEventDTO(
            user_id=user.user_id,
            in_watchlist=True,
            produce_timestamp=datetime.now(),
            **watchlist.model_dump(),
        )
        key = self._get_key( watchlist, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(watchlist)
        await self.producer.send(self.topic, key, message)

        return watchlist

class RemoveFromWatchlistService(BaseService):

    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'mongo'

    async def execute(self, watchlist: WatchlistEventDTO, user: User) -> DeleteWatchlistEventDTO:
        watchlist = DeleteWatchlistEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.now(),
            **watchlist.model_dump(),
        )
        key = self._get_key( watchlist, include_fields=['user_id', 'film_id', 'produce_timestamp'])
        message = self._get_message(watchlist)
        await self.producer.send(self.topic, key, message)

        return watchlist

class GetWatchlistService(BaseService):

    def __init__(self, producer: AbstractSortProducer) -> None:
        self.producer = producer
        self.collection = 'watchlist'

    async def execute(self, user: User) -> list[WatchlistEventDTO]:
        watchlist = await self.producer.get(self.collection, user.user_id, WatchlistEventDTO)

        return watchlist

@lru_cache()
def add_to_watchlist_service(
        producer: AbstractProducer = Depends(get_producer),
) -> AddToWatchlistService:
    return AddToWatchlistService(producer=producer)

@lru_cache()
def remove_from_watchlist_service(
        producer: AbstractProducer = Depends(get_producer),
) -> RemoveFromWatchlistService:
    return RemoveFromWatchlistService(producer=producer)

@lru_cache()
def get_wathlist_service(
        producer: AbstractSortProducer = Depends(get_mongo_producer),
) -> GetWatchlistService:
    return GetWatchlistService(producer=producer)
