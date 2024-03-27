from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from services.produce_film_quality_service import get_produce_film_quality_servece, ProduceFilmQualitySevice
from models.film_quality import FilmQualityEventDTO, FilmQualityEventResponse
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
        await service.execute(film_quality=film_quality, user=user)
    except exceptions.FilmNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Фильм не был найден')
    return FilmQualityEventResponse(film_id=film_quality.film_id)
