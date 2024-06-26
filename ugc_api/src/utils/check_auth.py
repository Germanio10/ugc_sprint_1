from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import MissingTokenError, JWTDecodeError
from fastapi import HTTPException
from starlette import status
from fastapi import Request

from models.user import User


class CheckAuth(AuthJWT):
    async def __call__(self, request: Request) -> User:
        self._request = request
        try:
            await self.jwt_required()
            user_id = await self.get_jwt_subject()
            role_id = (await self.get_raw_jwt())["role_id"]
            return User(user_id=user_id, role_id=role_id, cookies=self._request.cookies)

        except MissingTokenError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not authorized",
            )

        except JWTDecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid",
            )
