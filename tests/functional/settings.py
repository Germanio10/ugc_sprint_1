from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(f"{BASE_DIR}/.env")


class TestKafkaSettings(BaseSettings):
    kafka_hosts: str = Field(validation_alias='KAFKA_HOSTS', default='localhost:9094')
    topics: list[str] = Field(validation_alias='TOPICS', default=[])
    num_partitions: int = Field(validation_alias='NUM_PARTITIONS', default=3)
    replication_factor: int = Field(validation_alias='REPLICATION_FACTOR', default=3)

    @property
    def kafka_hosts_as_list(self) -> list[str]:
        return self.kafka_hosts.split(',')


class TestAuthServiceSettings(BaseSettings):
    host: str = Field(validation_alias='FASTAPI_AUTH_HOST')
    port: int = Field(validation_alias='FASTAPI_AUTH_PORT')

    def url(self):
        return f'http://{self.host}:{self.port}/api/v1'


class TestUGCServiceSettings(BaseSettings):
    host: str = Field(validation_alias='FASTAPI_UGC_HOST')
    port: int = Field(validation_alias='FASTAPI_UGC_PORT')

    def url(self):
        return f'http://{self.host}:{self.port}/api/v1'


class TestSettings(BaseSettings):
    kafka: TestKafkaSettings = TestKafkaSettings()
    auth_service: TestAuthServiceSettings = TestAuthServiceSettings()
    ugc_service: TestUGCServiceSettings = TestUGCServiceSettings()


settings = TestSettings()
