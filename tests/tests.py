import json
from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import AsyncMock

from fastapi import Request

from src.gspot_fastapi_auth.auth import UserRedisAuth
from src.gspot_fastapi_auth.providers import RedisClient
from src.gspot_fastapi_auth.services import TokenService
from src.gspot_fastapi_auth.settings import token_config
from src.gspot_fastapi_auth.test_factory import AdminUserFactory, CustomerUserFactory, DeveloperUserFactory


class TestRedisService(IsolatedAsyncioTestCase):

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_010_get_token(self, redis_mock):
        redis_client = RedisClient(
            token_config.HOST,
            token_config.PORT,
            token_config.DB,
            token_config.PASSWORD
        )
        token_service = TokenService(redis_client.session)
        mock_value = b'{"123": "123"}'
        redis_mock.return_value = mock_value
        value = await token_service.get_token_data('123')
        self.assertEqual(json.loads(mock_value), value)

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_020_get_valid_from_headers(self, redis_mock):
        token_config.TOKEN_STORAGE = 'headers'
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        mock_request = mock.create_autospec(Request)
        mock_request.headers.get.return_value = '123'
        auth_service = UserRedisAuth()
        user = await auth_service(mock_request)
        admin_data.pop('role')
        self.assertEqual(admin_data, user.to_dict())

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_030_valid_from_cookies(self, redis_mock):
        token_config.TOKEN_STORAGE = 'cookies'
        customer_data = CustomerUserFactory().to_dict()
        customer_data['role'] = 'customer'
        redis_mock.return_value = json.dumps(customer_data)
        mock_request = mock.create_autospec(Request)
        mock_request.cookies.get.return_value = '123'
        auth_service = UserRedisAuth()
        user = await auth_service(mock_request)
        customer_data.pop('role')
        self.assertEqual(customer_data, user.to_dict())

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_040_valid_from_cookies(self, redis_mock):
        token_config.TOKEN_STORAGE = 'headers'
        developer_data = DeveloperUserFactory().to_dict()
        developer_data['company'] = {}
        developer_data['role'] = 'developer'
        redis_mock.return_value = json.dumps(developer_data)
        mock_request = mock.create_autospec(Request)
        mock_request.headers.get.return_value = '123'
        auth_service = UserRedisAuth()
        user = await auth_service(mock_request)
        developer_data.pop('role')
        self.assertEqual(developer_data, user.to_dict())
