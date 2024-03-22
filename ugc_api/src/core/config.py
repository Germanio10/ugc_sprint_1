import logging

from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    kafka_host: str = Field(validation_alias='KAFKA_HOST', default='localhost:9094')
    topics: list[str] = Field(validation_alias='TOPICS', default=[])
    num_partitions: int = Field(validation_alias='NUM_PARTITIONS', default=3)
    replication_factor: int = Field(validation_alias='REPLICATION_FACTOR', default=3)


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    log_level: int | str = Field(validation_alias='LOG_LEVEL', default=logging.DEBUG)


settings = Settings()
