from aiokafka import AIOKafkaProducer


kafka: AIOKafkaProducer | None = None


def get_kafka() -> AIOKafkaProducer:
    return kafka
