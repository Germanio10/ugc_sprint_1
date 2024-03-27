from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from services.produce_film_quality_service import get_produce_film_quality_servece, ProduceFilmQualitySevice
from services.filter_service import get_search_filter_servece, SearchFilterSevice
from models.film_quality import FilmQualityEventDTO, FilmQualityEventResponse
from models.filter import FilterEventDTO, FilterEventResponse
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


@router.post('/search_filter/',
             response_model=FilterEventResponse,
             description="Фильтры, используемые в поиске",
             status_code=HTTPStatus.CREATED
             )
async def process_search_filter(
    search_filter: FilterEventDTO = Body(),
    user: User = Depends(CheckAuth()),
    service: SearchFilterSevice = Depends(
        get_search_filter_servece),

):
    try:
        await service.execute(search_filter=search_filter, user=user)
    except exceptions.GenreNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Жанр не был найден')
    return FilterEventResponse(genre_id=search_filter.genre_id)
