from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from services.likes import LikeService, get_like_service
from models.likes import LikeInfoEventDTO
from models.user import User
from models.response_message import ResponseMessage
from utils.messages import MESSAGE
from utils.check_auth import CheckAuth


router = APIRouter()


@router.post('/like/',
             response_model=ResponseMessage,
             description='Лайк или дизлайк',
             status_code=HTTPStatus.CREATED)
async def like(
        like_info: LikeInfoEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: LikeService = Depends(get_like_service)
):
    await service.execute(like=like_info, user=user)
    return ResponseMessage(message=MESSAGE)
