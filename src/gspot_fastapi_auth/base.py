import json


class BaseRedis:
    def __init__(self, session):
        self.session = session

    async def _get(self, key: str):
        response = await self.session.get(key)
        if response:
            return json.loads(response)
        else:
            return {}

    async def _put(self, key: str, data: dict):
        return await self.session.set(key, json.dumps(data))
