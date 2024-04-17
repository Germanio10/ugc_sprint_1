from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, Path, HTTPException
from services.rating_service import (RatingService, get_rating_service,
                                     DeleteRatingService, get_delete_rating_service, AverageRatingService,
                                     get_average_rating_service)
from models.rating import RatingInfoEventDTO, RatingDeleteInfoEventDTO, AverageRating
from models.user import User
from models.response_message import ResponseMessage
from utils.messages import MESSAGE, DELETE_MESSAGE
from utils.check_auth import CheckAuth


router = APIRouter()


@router.post('/rating/',
             response_model=ResponseMessage,
             description='Выставить оценку фильма',
             status_code=HTTPStatus.CREATED)
async def rating(
        rating_info: RatingInfoEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: RatingService = Depends(get_rating_service)
):
    await service.execute(rating=rating_info, user=user)
    return ResponseMessage(message=MESSAGE)


@router.delete('/delete_rating/',
               response_model=ResponseMessage,
               description='Удаление оценки у фильма',
               status_code=HTTPStatus.ACCEPTED)
async def delete_rating(
        delete_rating_info: RatingDeleteInfoEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: DeleteRatingService = Depends(get_delete_rating_service)
):
    await service.execute(delete_rating=delete_rating_info, user=user)
    return ResponseMessage(message=DELETE_MESSAGE)


@router.get('/average_rating/{film_id}',
            response_model=AverageRating,
            description='Средний рейтинг фильма',
            status_code=HTTPStatus.OK)
async def average_rating(
        film_id: str = Path(title="UUID фильма"),
        user: User = Depends(CheckAuth()),
        service: AverageRatingService = Depends(get_average_rating_service),
):
    result = await service.get_average_rating(film_id=film_id, user=user)
    if result:
        return result
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='На этот фильм нет отзывов')
