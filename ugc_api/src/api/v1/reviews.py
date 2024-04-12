from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from services.reviews_service import add_to_reviews_service, AddToReviewsService
from models.reviews import ReviewsEventDTO
from models.user import User
from models.response_message import ResponseMessage
from utils.messages import MESSAGE
from utils.check_auth import CheckAuth


router = APIRouter()


@router.post('/post_review/',
             response_model=ResponseMessage,
             description="Добавление отзыва",
             status_code=HTTPStatus.CREATED
             )
async def watchlist_post(
        review: ReviewsEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: AddToReviewsService = Depends(add_to_reviews_service)
):
    await service.execute(review=review, user=user)
    return ResponseMessage(message=MESSAGE)


# @router.post('/delete_watchlist/',
#              response_model=ResponseMessage,
#              description="Добавление лайка к отзыву",
#              status_code=HTTPStatus.CREATED
#              )
# async def watchlist_delete(
#         watchlist: WatchlistEventDTO = Body(),
#         user: User = Depends(CheckAuth()),
#         service: RemoveFromWatchlistService = Depends(remove_from_watchlist_service)
# ):
#     await service.execute(watchlist=watchlist, user=user)
#     return ResponseMessage(message=MESSAGE)
