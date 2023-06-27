import redis.asyncio as redis

from .settings import token_config


class RedisClient:
    def __init__(self, host: str, port: int, db: int, password: str):
        self.session = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
        )

    async def close(self):
        await self.session.close()


class RedisSingleton:
    _instance: RedisClient = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = RedisClient(
                token_config.HOST,
                token_config.PORT,
                token_config.DB,
                token_config.PASSWORD,
            )
        return cls._instance

    @classmethod
    def init_redis(cls, host: str, port: int, db: int, password: str):
        cls._instance = RedisClient(host, port, db, password)
