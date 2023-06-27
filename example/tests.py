import json
from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from src.gspot_fastapi_auth import token_config, BaseRedis
from src.gspot_fastapi_auth.providers import RedisClient
from src.gspot_fastapi_auth.test_factory import AdminUserFactory, CustomerUserFactory, DeveloperUserFactory

from main import app


class TestAuth(IsolatedAsyncioTestCase):
    url = '/'
    customer_url = '/customer/'

    async def asyncSetUp(self) -> None:
        self.client = TestClient(app)

    async def test_010_get_without_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_15_get_from_headers(self, redis_mock):
        token_config.TOKEN_STORAGE = 'headers'
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        response = self.client.get(self.url, headers={'HTTP_AUTHORIZATION': '12345'})
        result = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        admin_data.pop('role')
        self.assertEqual(result, admin_data)

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_020_get_from_cookies(self, redis_mock):
        token_config.TOKEN_STORAGE = 'cookies'
        self.client.cookies.set('Authentication', '123')
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        response = self.client.get(self.url)
        result = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        admin_data.pop('role')
        self.assertEqual(result, admin_data)

    async def test_030_get_data_from_redis(self):
        customer_data = CustomerUserFactory().to_dict()
        customer_data['role'] = 'customer'
        token_config.TOKEN_STORAGE = 'cookies'
        self.client.cookies.set('Authentication', 'access_token')
        redis_client = RedisClient(
            token_config.HOST,
            token_config.PORT,
            token_config.DB,
            token_config.PASSWORD
        )
        base_redis = BaseRedis(redis_client.session)
        await base_redis._put('access_token', customer_data)
        with self.client as client:
            response = client.get('/')
        result = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        customer_data.pop('role')
        self.assertEqual(result, customer_data)

    async def test_035_get_developer_data_from_redis(self):
        developer_data = DeveloperUserFactory().to_dict()
        developer_data['role'] = 'developer'
        developer_data['company'] = {}
        token_config.TOKEN_STORAGE = 'cookies'
        self.client.cookies.set('Authentication', 'developer_token')
        redis_client = RedisClient(
            token_config.HOST,
            token_config.PORT,
            token_config.DB,
            token_config.PASSWORD
        )
        base_redis = BaseRedis(redis_client.session)
        await base_redis._put('developer_token', developer_data)
        with self.client as client:
            response = client.get('/')
        await redis_client.close()
        result = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        developer_data.pop('role')
        self.assertEqual(result, developer_data)

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_040_get_from_cookies(self, redis_mock):
        token_config.TOKEN_STORAGE = 'cookies'
        self.client.cookies.set('Authentication', '123')
        customer_data = CustomerUserFactory().to_dict()
        customer_data['role'] = 'customer'
        redis_mock.return_value = json.dumps(customer_data)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_050_test_permissions(self, redis_mock):
        token_config.TOKEN_STORAGE = 'cookies'
        self.client.cookies.set('Authentication', '123')
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 403)

    @mock.patch('redis.asyncio.Redis.get', new_callable=AsyncMock)
    async def test_060_test_developer(self, redis_mock):
        token_config.TOKEN_STORAGE = 'cookies'
        self.client.cookies.set('Authentication', '123')
        developer_data = DeveloperUserFactory().to_dict()
        developer_data['role'] = 'developer'
        redis_mock.return_value = json.dumps(developer_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
