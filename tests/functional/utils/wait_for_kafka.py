import os

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()


def connect_kafka(hosts: list[str]):
    print('Ожидание kafka...')
    producer = KafkaProducer(bootstrap_servers=hosts)
    producer.bootstrap_connected()


if __name__ == "__main__":

    hosts = os.getenv("KAFKA_HOSTS") or 'localhost:9094'

    connect_kafka(hosts.split(','))
