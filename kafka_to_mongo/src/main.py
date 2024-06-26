from config import settings
from extractor import Extractor
from kafka import KafkaConsumer
from loader import Loader
from pipline import ETL
from pymongo import MongoClient

if __name__ == '__main__':
    consumer = KafkaConsumer(
        bootstrap_servers=settings.kafka.kafka_hosts_as_list,
        auto_offset_reset='earliest',
        max_poll_records=500,
        enable_auto_commit=False,
        group_id=settings.kafka.group_id,
    )
    consumer.subscribe(["mongo"])

    mongo = MongoClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
    db = mongo['UGC']

    etl = ETL(extractor=Extractor(consumer), loader=Loader(db))
    etl.run()
