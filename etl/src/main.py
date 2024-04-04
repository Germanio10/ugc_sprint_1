from clickhouse_driver import Client
from kafka import KafkaConsumer

from clickhouse_client import Clickhouse
from logger import logger
from loader import Loader
from extractor import Extractor
from pipline import ETL
from config import settings


if __name__ == '__main__':
    consumer = KafkaConsumer(
     bootstrap_servers=settings.kafka.kafka_hosts_as_list,
     auto_offset_reset='earliest',
     max_poll_records=500,
     enable_auto_commit=False,
     group_id=settings.kafka.group_id
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
    etl.run()
