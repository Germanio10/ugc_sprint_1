from contextlib import asynccontextmanager
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from core.logger import LOGGING
from core.config import settings
from client_kafka import create_topics


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_topics()
    yield


app = FastAPI(
    title='UGC сервис',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description="Сервис, предоставляющий API для сбора аналитической информации",
    version="1.0.0",
    lifespan=lifespan
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.log_level
    )