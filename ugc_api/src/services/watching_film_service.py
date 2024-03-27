from datetime import datetime
from services.base_service import BaseService
from producers.abstract_producer import AbstractProducer
from clients.api_client import ApiClient, get_api_client
from models.film_progress import FilmProgressEventDTO
from fastapi import Depends, HTTPException
from core import exceptions
from models.film_progress import FilmProgressProduceEventDTO
from functools import lru_cache
from producers.kafka_producer import get_producer
from models.user import User


class WatchingFilmService(BaseService):

    def __init__(self, producer: AbstractProducer, api_client: ApiClient) -> None:
        self.producer = producer
        self.api_client = api_client
        self.topic = 'messages'

    async def execute(self, film_progress: FilmProgressEventDTO, user: User) -> FilmProgressProduceEventDTO:
        path = f'/api/v1/films/{film_progress.film_id}/'

        try:
            film = await self.api_client.get(path=path, cookies=user.cookies)
        except HTTPException:
            raise exceptions.FilmNotFoundError

        film_progress = FilmProgressProduceEventDTO(
            user_id=user.user_id,
            title=film['title'],
            imdb_rating=film['imdb_rating'],
            genre=film['genre'],
            produce_timestamp=datetime.now(),
            **film_progress.model_dump(),
        )
        key = self._get_key(film_progress, exclude_fields=['genre', 'produce_timestamp', ])
        message = self._get_message(film_progress)
        await self.producer.send(self.topic, key, message)

        return film_progress


@lru_cache()
def get_watching_film_service(
        producer: AbstractProducer = Depends(get_producer),
        api_client: ApiClient = Depends(get_api_client)
) -> WatchingFilmService:
    return WatchingFilmService(producer=producer, api_client=api_client)
