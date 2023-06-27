import json


class BaseRedis:
    def __init__(self, session):
        self.session = session

    async def _get(self, key: str):
        async with self.session() as s:
            response = await s.get(key)
            if response:
                return json.loads(response)
            else:
                return {}

    async def _put(self, key: str, data: dict):
        async with self.session() as s:
            return await s.set(key, json.dumps(data))
