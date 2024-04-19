from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    kafka_hosts: str = Field(validation_alias='KAFKA_HOSTS', default='localhost:9094')
    topic: list[str] = Field(validation_alias='TOPIC_FOR_MONGO', default=[])
    group_id: str = Field(validation_alias='GROUP_ID_FOR_MONGO', default='kafka_to_mongo')

    @property
    def kafka_hosts_as_list(self) -> list[str]:
        return self.kafka_hosts.split(',')


class MongoSettings(BaseSettings):
    host: str = Field(validation_alias='MONGO_HOST', default='localhost')
    port: int = Field(validation_alias='MONGO_PORT', default=27017)


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    mongo: MongoSettings = MongoSettings()


settings = Settings()
