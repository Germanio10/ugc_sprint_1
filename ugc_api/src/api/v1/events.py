from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from services.produce_film_quality_service import get_produce_film_quality_servece, ProduceFilmQualitySevice
from services.watching_film_service import get_watching_film_service, WatchingFilmService
from models.film_quality import FilmQualityEventDTO, FilmQualityEventResponse
from models.film_progress import FilmProgressEventResponse, FilmProgressEventDTO
from core import exceptions
from models.user import User
from utils.check_auth import CheckAuth

router = APIRouter()


@router.post('/film_quality/',
             response_model=FilmQualityEventResponse,
             description="Изменеие качества видео",
             status_code=HTTPStatus.CREATED
             )
async def produce_film_quality(
    film_quality: FilmQualityEventDTO = Body(),
    user: User = Depends(CheckAuth()),
    service: ProduceFilmQualitySevice = Depends(
        get_produce_film_quality_servece),

):
    try:
        await service.execute(film_quality=film_quality, user_id=user.user_id)
    except exceptions.FilmNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Фильм не был найден')
    return FilmQualityEventResponse(film_id=film_quality.film_id)


@router.post('/watching_film_progress/',
             response_model=FilmProgressEventResponse,
             description="Время и проценты от просмотра фильма",
             status_code=HTTPStatus.CREATED
             )
async def watching_film_progress(
        film_progress: FilmProgressEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: WatchingFilmService = Depends(get_watching_film_service)
):
    try:
        await service.execute(film_progress=film_progress, user_id=user.user_id)
    except exceptions.FilmNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Фильм не был найден')
    return FilmProgressEventResponse(film_id=film_progress.film_id)