from typing import Type

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import BaseUser, UserFactory
from .providers import RedisSingleton
from .services import TokenService
from .settings import token_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class UserRedisAuth(HTTPBearer):
    @staticmethod
    def _get_token_from_headers(request: Request) -> str:
        token = request.headers.get('HTTP_AUTHORIZATION')
        if not token:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Not authenticated')
        return token

    @staticmethod
    def _get_token_from_cookies(request: Request) -> str:
        token = request.cookies.get('Authentication')
        if not token:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Not authenticated')
        return token

    async def __call__(self, request: Request) -> Type[BaseUser]:
        token_service = TokenService(RedisSingleton().session)
        if token_config.TOKEN_STORAGE == 'headers':
            token = self._get_token_from_headers(request)
        else:
            token = self._get_token_from_cookies(request)
        data = await token_service.get_token_data(token)
        if not data:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Not authenticated')
        user_class = UserFactory().get_user(data.pop('role'))
        return user_class(**data)


__all__ = [
    'UserRedisAuth',
]
