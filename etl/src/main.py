from clickhouse_driver import Client
from kafka import KafkaConsumer

from clickhouse_client import Clickhouse
from logger import logger
from state.json_file_storage import JsonFileStorage
from state.models import State
from loader import Loader
from extractor import Extractor
from pipline import ETL
from config import settings


if __name__ == '__main__':
    state = State(JsonFileStorage(logger=logger))
    consumer = KafkaConsumer(
     bootstrap_servers=settings.kafka.kafka_hosts_as_list,
     auto_offset_reset='earliest',
     max_poll_records=500,
    )
    consumer.subscribe(settings.kafka.topics)

    client_clickhouse = Client(
                                host=settings.clickhouse.main_host,
                                port=settings.clickhouse.port,
                                alt_hosts=settings.clickhouse.alt_hosts,
                                round_robin=True
                               )

    clickhouse = Clickhouse(client_clickhouse)
    clickhouse.init_database()

    etl = ETL(extractor=Extractor(consumer), loader=Loader(clickhouse))
    etl.run(state)
