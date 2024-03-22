import logging


from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from core.config import settings

logger = logging.getLogger(__name__)


def create_topics():
    """Создание топиков kafka"""

    logger.info('Создание топиков...')

    client = KafkaAdminClient(bootstrap_servers=settings.kafka.kafka_host)

    topics = [NewTopic(name=topic, num_partitions=settings.kafka.num_partitions,
                       replication_factor=settings.kafka.replication_factor) for topic in settings.kafka.topics]

    try:
        client.create_topics(new_topics=topics, validate_only=False)
    except TopicAlreadyExistsError as err:
        logger.info('Топики уже существуют: {}'.format(err))
    except Exception as e:
        logger.error('Ошибка создания топиков {}'.format(err))

        
