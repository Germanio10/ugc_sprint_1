from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
from aiohttp import client
from async_fastapi_jwt_auth import AuthJWT
import uvicorn

from core.logger import LOGGING
from core.config import JWTSettings, settings
from api.v1 import events
from db import kafka
from clients import api_session, admin_client_kafka


@asynccontextmanager
async def lifespan(app: FastAPI):
    admin_client_kafka.AdminClientKafka.create_topics(settings.kafka.topics)
    api_session.session = client.ClientSession()
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=settings.kafka.kafka_hosts_as_list)

    await kafka.kafka.start()
    yield
    await kafka.kafka.stop()
    await api_session.session.close()


app = FastAPI(
    title='UGC сервис',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description="Сервис, предоставляющий API для сбора аналитической информации",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(events.router, prefix='/api/v1', tags=['events'])



@AuthJWT.load_config
def get_config():
    return JWTSettings()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.log_level
    )