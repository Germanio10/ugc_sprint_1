from pymongo import MongoClient
from kafka import KafkaProducer
from core.config import settings


class RatingCalculator:
    def __init__(self):
        self.mongo_client = MongoClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        self.kafka_producer = KafkaProducer(bootstrap_servers=settings.kafka.kafka_hosts)
        self.kafka_topic = settings.kafka.topic_for_mongo

    async def calculate_average_rating(self):
        db = self.mongo_client['UGC']
        collection = db['rating']
        pipeline = [
            {"$group": {"_id": "$film_id", "average_rating": {"$avg": "$rating"}}}
        ]
        cursor = collection.aggregate(pipeline)
        print(cursor)
        for rating in cursor:
            film_id = rating['_id']
            average_rating = rating['average_rating']
            self.send_to_kafka(film_id, average_rating)

    def send_to_kafka(self, film_id, average_rating):
        message = {'film_id': film_id, 'average_rating': average_rating}
        self.kafka_producer.send(self.kafka_topic, key=str(film_id).encode(), value=message)
