import os

from pydantic import BaseSettings


class TokenSettings(BaseSettings):
    host: str = os.getenv('REDIS_AUTH_HOST', '127.0.0.1')
    port: int = int(os.getenv('REDIS_AUTH_PORT', 6379))
    password: str = os.getenv('REDIS_AUTH_PASSWORD', None)
    db: int = int(os.getenv('REDIS_AUTH_DB', 0))
    prefix: str = os.getenv('REDIS_ACCESS_PREFIX', '')
    storage: str = os.getenv('TOKEN_STORAGE', 'headers')


token_config = TokenSettings()

__all__ = [
    'token_config',
]
