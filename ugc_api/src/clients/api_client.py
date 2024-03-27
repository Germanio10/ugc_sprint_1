from functools import lru_cache
from http import HTTPStatus
import aiohttp
from fastapi import Depends, HTTPException
from pydantic import BaseModel

from clients.api_session import get_api_session
from core.config import settings


class ApiResponse(BaseModel):
    status: int
    body: dict
    headers: dict


class ApiClient:
    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        self.base_url = base_url
        self.session = session

    async def get(self, path, cookies,  **kwargs) -> aiohttp.ClientResponse:
        url = f'{self.base_url}{path}'
        async with self.session.get(url, cookies=cookies, params={**kwargs},) as response:
            if response.status != HTTPStatus.OK:
                raise HTTPException(status_code=response.status)
            return await response.json()


@lru_cache
def get_api_client(
    session: aiohttp.ClientSession = Depends(get_api_session)
) -> ApiClient:
    return ApiClient(base_url=settings.films_api_base_url, session=session)