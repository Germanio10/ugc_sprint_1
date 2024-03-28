from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from services.produce_film_quality_service import get_produce_film_quality_servece, ProduceFilmQualityService
from services.watching_film_service import get_watching_film_service, WatchingFilmService
from services.click_tracking_service import get_click_tracking_service, ClickTrackingService
from models.film_quality import FilmQualityEventDTO
from models.film_progress import FilmProgressEventDTO
from models.click_info import ClickInfoEventDTO
from models.user import User
from models.response_message import ResponseMessage
from utils.messages import MESSAGE
from utils.check_auth import CheckAuth


router = APIRouter()


@router.post('/film_quality/',
             response_model=ResponseMessage,
             description="Изменеие качества видео",
             status_code=HTTPStatus.CREATED
             )
async def produce_film_quality(
    film_quality: FilmQualityEventDTO = Body(),
    user: User = Depends(CheckAuth()),
    service: ProduceFilmQualityService = Depends(
        get_produce_film_quality_servece),

):
    await service.execute(film_quality=film_quality, user=user)
    return ResponseMessage(message=MESSAGE)


@router.post('/watching_film_progress/',
             response_model=ResponseMessage,
             description="Время и проценты от просмотра фильма",
             status_code=HTTPStatus.CREATED
             )
async def watching_film_progress(
        film_progress: FilmProgressEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: WatchingFilmService = Depends(get_watching_film_service)
):
    await service.execute(film_progress=film_progress, user=user)
    return ResponseMessage(message=MESSAGE)


@router.post('/click_tracking/',
             response_model=ResponseMessage,
             description="Отслеживание кликов юзера",
             status_code=HTTPStatus.CREATED
             )
async def click_tracking(
        click_info: ClickInfoEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: ClickTrackingService = Depends(get_click_tracking_service)
):
    await service.execute(click_info=click_info, user=user)
    return ResponseMessage(message=MESSAGE)
