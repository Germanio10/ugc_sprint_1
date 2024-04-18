from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, Query
from services.reviews_service import add_to_reviews_service, AddToReviewsService, reviews_rating_service, ReviewsRatingService, GetReviewsService, get_reviews_service
from models.reviews import ReviewsEventDTO, RatingInfoEventDTO,  ReviewsResposeDTO
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


@router.post('/rate_review/',
             response_model=ResponseMessage,
             description="Оценка отзыва",
             status_code=HTTPStatus.CREATED
             )
async def rate_review(
        rating_info: RatingInfoEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: ReviewsRatingService = Depends(reviews_rating_service)
):
    await service.execute(rating=rating_info, user=user)
    return ResponseMessage(message=MESSAGE)

@router.get('/get_reviews/',
             response_model=list[ReviewsResposeDTO],
             description="Список всех отзывов",
             status_code=HTTPStatus.CREATED
             )
async def watchlist_get(
        field: str = Query(),
        ascending: bool = Query(),
        user: User = Depends(CheckAuth()),
        service: GetReviewsService = Depends(get_reviews_service)
) -> list[ReviewsResposeDTO]:
    reviews = await service.execute(user=user, field=field, ascending=ascending)
    return reviews
