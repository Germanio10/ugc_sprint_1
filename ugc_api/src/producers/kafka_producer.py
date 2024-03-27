from functools import lru_cache
from aiokafka import AIOKafkaProducer
from fastapi import Depends

from producers.abstract_producer import AbstractProducer
from db.kafka import get_kafka


class KafkaProducer(AbstractProducer):

    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    async def send(self, topic: str, key: bytes, message: bytes):
        await self.producer.send_and_wait(topic, message, key)


@lru_cache()
def get_producer(producer: AIOKafkaProducer = Depends(get_kafka)) -> AbstractProducer:
    return KafkaProducer(producer)
