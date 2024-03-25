from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from services.produce_film_quality_service import get_produce_film_quality_servece, ProduceFilmQualitySevice
from models.film_quality import FilmQualityEventDTO, FilmQualityEventResponse
from core import exceptions

router = APIRouter()


@router.post('/film_quality/',
             response_model=FilmQualityEventResponse,
             description="Изменеие качества видео",
             status_code=HTTPStatus.CREATED
             )
async def produce_film_quality(
    film_quality: FilmQualityEventDTO,
    service: ProduceFilmQualitySevice = Depends(
        get_produce_film_quality_servece)
) -> dict:
    try:
        await service.execute(film_quality=film_quality)
    except exceptions.FilmNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Фильм не был найден')
    return FilmQualityEventResponse(film_id=film_quality.film_id)
