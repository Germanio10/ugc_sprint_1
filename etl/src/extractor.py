from kafka import KafkaConsumer


from datetime import datetime
from logger import logger


import json


class Extractor:
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer
        self.events_time = []

    def extract(self, last_produce_time: datetime) -> tuple[list, datetime]:
        messages = []
        records = self.consumer.poll(10.0)
        self.events_time.append(last_produce_time)

        for _, consumer_records in records.items():
            for record in consumer_records:
                if record.value:
                    try:
                        record = json.loads(record.value.decode('utf-8'))
                        if not record.get('produce_timestamp'):
                            continue
                        event_time = datetime.strptime(record.get('produce_timestamp'), '%Y-%m-%dT%H:%M:%S.%f')
                        if event_time > last_produce_time:
                            messages.append(record)
                            self.events_time.append(event_time)
                    except json.decoder.JSONDecodeError:
                        logger.warning("Format message is not correct")
        if not messages:
            last_produce_time = max(self.events_time)
            self.events_time.clear()
        return messages, last_produce_time
