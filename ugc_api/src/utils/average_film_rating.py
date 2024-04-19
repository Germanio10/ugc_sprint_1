import json
import threading
import time

from core.config import settings
from kafka import KafkaProducer
from pymongo import MongoClient


class RatingCalculator(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        self.kafka_producer = KafkaProducer(bootstrap_servers=settings.kafka.kafka_hosts)
        self.kafka_topic = 'mongo'

    def run(self):
        while True:
            db = self.mongo_client['UGC']
            collection = db['rating']
            pipeline = [{"$group": {"_id": "$film_id", "average_rating": {"$avg": "$rating"}}}]
            cursor = collection.aggregate(pipeline)
            for rating in cursor:
                film_id = rating['_id']
                average_rating = rating['average_rating']
                self.send_to_kafka(film_id, average_rating)
            time.sleep(10)

    def send_to_kafka(self, film_id, average_rating):
        message = {'film_id': film_id, 'average_rating': average_rating}
        self.kafka_producer.send(
            self.kafka_topic, key=str(film_id).encode(), value=json.dumps(message).encode()
        )
