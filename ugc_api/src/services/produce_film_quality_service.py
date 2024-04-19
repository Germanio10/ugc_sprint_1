from datetime import datetime
from functools import lru_cache

from clients.api_client import ApiClient, get_api_client
from fastapi import Depends
from models.film_quality import FilmQualityEventDTO, FilmQualityProduceEventDTO
from models.user import User
from producers.abstract_producer import AbstractProducer
from producers.kafka_producer import get_producer
from services.base_service import BaseService


class ProduceFilmQualityService(BaseService):
    def __init__(self, producer: AbstractProducer, api_client: ApiClient) -> None:
        self.producer = producer
        self.api_client = api_client
        self.topic = 'messages'

    async def execute(
        self,
        film_quality: FilmQualityEventDTO,
        user: User,
    ) -> FilmQualityProduceEventDTO:
        film_quality = FilmQualityProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.now(),
            **film_quality.model_dump(),
        )

        key = self._get_key(
            film_quality,
            include_fields={
                'user_id',
                'film_id',
                'produce_timestamp',
            },
        )
        message = self._get_message(film_quality)
        await self.producer.send(self.topic, key, message)

        return film_quality


@lru_cache
def get_produce_film_quality_servece(
    producer: AbstractProducer = Depends(get_producer),
    api_client: ApiClient = Depends(get_api_client),
) -> ProduceFilmQualityService:
    return ProduceFilmQualityService(producer=producer, api_client=api_client)
