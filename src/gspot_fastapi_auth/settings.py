from pydantic import BaseSettings


class TokenSettings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 6379
    PASSWORD: str = None
    DB: int = 0
    ACCESS_PREFIX: str = ''
    TOKEN_STORAGE: str = 'headers'

    class Config:
        env_prefix = 'REDIS_AUTH_'


token_config = TokenSettings()

__all__ = [
    'token_config',
]
