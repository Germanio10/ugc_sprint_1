from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from services.watchlist_service import add_to_watchlist_service, remove_from_watchlist_service,AddToWatchlistService, RemoveFromWatchlistService, GetWatchlistService, get_wathlist_service
from models.watchlist import WatchlistEventDTO
from models.user import User
from models.response_message import ResponseMessage
from utils.messages import MESSAGE, DELETE_MESSAGE
from utils.check_auth import CheckAuth


router = APIRouter()


@router.post('/post_watchlist/',
             response_model=ResponseMessage,
             description="Добавление в закладки",
             status_code=HTTPStatus.CREATED
             )
async def watchlist_post(
        watchlist: WatchlistEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: AddToWatchlistService = Depends(add_to_watchlist_service)
):
    await service.execute(watchlist=watchlist, user=user)
    return ResponseMessage(message=MESSAGE)


@router.delete('/delete_watchlist/',
             response_model=ResponseMessage,
             description="Удаление из закладок",
             status_code=HTTPStatus.CREATED
             )
async def watchlist_delete(
        watchlist: WatchlistEventDTO = Body(),
        user: User = Depends(CheckAuth()),
        service: RemoveFromWatchlistService = Depends(remove_from_watchlist_service)
):
    await service.execute(watchlist=watchlist, user=user)
    return ResponseMessage(message=DELETE_MESSAGE)

@router.get('/get_watchlist/',
             response_model=list[WatchlistEventDTO],
             description="Список всех закладок",
             status_code=HTTPStatus.CREATED
             )
async def watchlist_get(
        user: User = Depends(CheckAuth()),
        service: GetWatchlistService = Depends(get_wathlist_service)
) -> list[WatchlistEventDTO]:
    watchlist = await service.execute(user=user)
    return watchlist
