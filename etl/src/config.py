from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    kafka_hosts: str = Field(
        validation_alias='KAFKA_HOSTS', default='localhost:9094')
    topics: list[str] = Field(validation_alias='TOPICS', default=[])

    @property
    def kafka_hosts_as_list(self) -> list[str]:
        return self.kafka_hosts.split(',')


class ClickhouseSettings(BaseSettings):
    main_host: str = Field(
        validation_alias='CLICKHOUSE_MAIN_HOST', default='localhost')
    port: str = Field(validation_alias='CLICKHOUSE_MAIN_PORT',
                      default='localhost')


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    clickhouse: ClickhouseSettings = ClickhouseSettings()


settings = Settings()
