from datetime import datetime
from functools import lru_cache

from fastapi import Depends
from models.film_progress import FilmProgressEventDTO, FilmProgressProduceEventDTO
from models.user import User
from producers.abstract_producer import AbstractProducer
from producers.kafka_producer import get_producer
from services.base_service import BaseService


class WatchingFilmService(BaseService):
    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'messages'

    async def execute(
        self,
        film_progress: FilmProgressEventDTO,
        user: User,
    ) -> FilmProgressProduceEventDTO:
        film_progress = FilmProgressProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.now(),
            **film_progress.model_dump(),
        )
        key = self._get_key(
            film_progress,
            include_fields={'user_id', 'film_id', 'produce_timestamp'},
        )
        message = self._get_message(film_progress)
        await self.producer.send(self.topic, key, message)

        return film_progress


@lru_cache()
def get_watching_film_service(
    producer: AbstractProducer = Depends(get_producer),
) -> WatchingFilmService:
    return WatchingFilmService(producer=producer)
