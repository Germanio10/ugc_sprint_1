from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from aiohttp import client
from aiokafka import AIOKafkaProducer
from api.v1 import events
from async_fastapi_jwt_auth import AuthJWT
from clients import admin_client_kafka, api_session
from core.config import JWTSettings, settings
from core.logger import LOGGING
from db import kafka
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


if not settings.is_debug:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


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
    lifespan=lifespan,
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    if settings.is_debug:
        return response
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'}
        )
    return response


app.include_router(events.router, prefix='/api/v1', tags=['events'])


@AuthJWT.load_config
def get_config():
    return JWTSettings()


if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='0.0.0.0', port=8000, log_config=LOGGING, log_level=settings.log_level
    )
