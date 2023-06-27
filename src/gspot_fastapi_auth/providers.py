from contextlib import asynccontextmanager

import redis.asyncio as redis


class RedisClient:
    def __init__(self, host: str, port: int, db: int, password: str):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    @asynccontextmanager
    async def session(self):
        try:
            session = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
            )
            yield session
        finally:
            await session.close()
