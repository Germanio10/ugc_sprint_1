import logging

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    kafka_hosts: str = Field(validation_alias='KAFKA_HOSTS', default='localhost:9094')
    topics: list[str] = Field(validation_alias='TOPICS', default=[])
    num_partitions: int = Field(validation_alias='NUM_PARTITIONS', default=3)
    replication_factor: int = Field(validation_alias='REPLICATION_FACTOR', default=3)

    @property
    def kafka_hosts_as_list(self) -> list[str]:
        return self.kafka_hosts.split(',')


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    films_api_base_url: str = Field(
        validation_alias='FILMS_API_BASE_URL', default='http://127.0.0.1:81'
    )
    log_level: int | str = Field(validation_alias='LOG_LEVEL', default=logging.DEBUG)
    sentry_dsn: str = Field(validation_alias='SENTRY_DSN', default='')


settings = Settings()


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
