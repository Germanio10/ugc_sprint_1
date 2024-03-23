import os

import backoff
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


load_dotenv()


@backoff.on_exception(backoff.expo, NoBrokersAvailable)
def connect_kafka(hosts: list[str]):
    print('Ожидание kafka...')
    producer = KafkaProducer(bootstrap_servers=hosts)
    producer.bootstrap_connected()


if __name__ == "__main__":
    hosts = os.getenv("KAFKA_HOSTS").split(',')
    
    connect_kafka(hosts)
