from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
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


class TestUGCServiceSettings(BaseSettings):
    host: str = Field(validation_alias='FASTAPI_UGC_HOST', default='localhost')
    port: int = Field(validation_alias='FASTAPI_UGC_PORT', default=8000)

    def url(self):
        return f'http://{self.host}:{self.port}/api/v1'


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"


class TestSettings(BaseSettings):
    kafka: TestKafkaSettings = TestKafkaSettings()
    ugc_service: TestUGCServiceSettings = TestUGCServiceSettings()


test_settings = TestSettings()
