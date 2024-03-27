from datetime import datetime
from functools import lru_cache
from uuid import UUID
from fastapi import Depends, HTTPException
from producers.abstract_producer import AbstractProducer
from models.film_quality import FilmQualityEventDTO, FilmQualityProduceEventDTO
from producers.kafka_producer import get_producer
from services.base_service import BaseService
from clients.api_client import ApiClient, get_api_client
from core import exceptions
from models.user import User


class ProduceFilmQualitySevice(BaseService):
    def __init__(self, producer: AbstractProducer, api_client: ApiClient) -> None:
        self.producer = producer
        self.api_client = api_client
        self.topic = 'messages'

    async def execute(self, film_quality: FilmQualityEventDTO, user: User) -> FilmQualityProduceEventDTO:
        path = f'/api/v1/films/{film_quality.film_id}/'

        try: 
            film = await self.api_client.get(path=path, cookies=user.cookies)
        except HTTPException:
            raise exceptions.FilmNotFoundError

        film_quality = FilmQualityProduceEventDTO(
            user_id=user.user_id,
            title=film['title'],
            imdb_rating=film['imdb_rating'],
            genre=film['genre'],
            produce_timestamp=datetime.now(),
            **film_quality.model_dump(),
        )

        key = self._get_key(film_quality, exclude_fields=['genre', 'produce_timestamp',])
        message = self._get_message(film_quality)
        await self.producer.send(self.topic, key, message)

        return film_quality


@lru_cache
def get_produce_film_quality_servece(
    producer: AbstractProducer = Depends(get_producer),
    api_client: ApiClient = Depends(get_api_client)
) -> ProduceFilmQualitySevice:
    return ProduceFilmQualitySevice(producer=producer, api_client=api_client)
