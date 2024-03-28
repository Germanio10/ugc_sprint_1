from datetime import datetime
from functools import lru_cache

from fastapi import Depends

from producers.abstract_producer import AbstractProducer
from producers.kafka_producer import get_producer
from services.base_service import BaseService
from models.user import User
from models.click_info import ClickInfoEventDTO, ClickInfoProduceEventDTO


class ClickTrackingService(BaseService):

    def __init__(self, producer: AbstractProducer) -> None:
        self.producer = producer
        self.topic = 'messages'

    async def execute(self, click_info: ClickInfoEventDTO, user: User) -> ClickInfoProduceEventDTO:

        click_info = ClickInfoProduceEventDTO(
            user_id=user.user_id,
            produce_timestamp=datetime.now(),
            **click_info.model_dump(),

        )
        key = self._get_key(click_info, exclude_fields=['produce_timestamp', ])
        message = self._get_message(click_info)
        await self.producer.send(self.topic, key, message)

        return click_info


@lru_cache()
def get_click_tracking_service(
        producer: AbstractProducer = Depends(get_producer),
) -> ClickTrackingService:
    return ClickTrackingService(producer=producer)
