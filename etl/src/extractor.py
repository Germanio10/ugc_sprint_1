import backoff

from kafka import KafkaConsumer, errors

from datetime import datetime
from logger import logger


import json


class Extractor:
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer

    @backoff.on_exception(
        backoff.expo,
        (errors.KafkaTimeoutError, errors.KafkaConnectionError, errors.KafkaConfigurationError),
    )
    def extract(self) -> list[dict]:
        messages = []
        records = self.consumer.poll(10.0)

        for _, consumer_records in records.items():
            for record in consumer_records:
                if record.value:
                    try:
                        record = json.loads(record.value.decode('utf-8'))
                        messages.append(record)
                    except json.decoder.JSONDecodeError:
                        logger.warning("Format message is not correct")
        return messages

    def commit(self):
        self.consumer.commit()
