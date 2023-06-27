from .base import BaseRedis
from .settings import token_config


class TokenService(BaseRedis):
    prefix = token_config.prefix

    async def get_token_data(self, token) -> dict:
        key = f'{self.prefix}:{token}' if self.prefix else token
        value = await self._get(key)
        return value
