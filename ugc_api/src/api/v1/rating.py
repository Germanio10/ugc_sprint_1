from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from services.rating_service import RatingService, get_rating_service
from models.rating import RatingInfoEventDTO
from models.user import User
from models.response_message import ResponseMessage
from utils.messages import MESSAGE
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
