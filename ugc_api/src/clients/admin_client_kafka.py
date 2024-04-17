import logging

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from core.config import settings


logger = logging.getLogger(__name__)


class AdminClientKafka:
    @staticmethod
    def create_topics(topics_name: list[str]):
        """Создание топиков kafka"""

        logger.info('Создание топиков')

        client = KafkaAdminClient(bootstrap_servers=settings.kafka.kafka_hosts_as_list)
        topics = [
            NewTopic(
                name=topic,
                num_partitions=settings.kafka.num_partitions,
                replication_factor=settings.kafka.replication_factor,
            )
            for topic in topics_name
        ]

        try:
            client.create_topics(new_topics=topics, validate_only=False)
        except TopicAlreadyExistsError as err:
            logger.info('Топики уже существуют: {}'.format(err))
        except Exception as e:
            logger.error('Ошибка создания топиков {}'.format(e))
