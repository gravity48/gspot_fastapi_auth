# GSpot authentication package

This package allows you to authorize users through a shared redis

## Install package
```shell
pip install gspot-fastapi-auth
```

## Define env variables

- `REDIS_AUTH_ACCESS_PREFIX` default ''
- `REDIS_AUTH_DB` default 0
- `REDIS_AUTH_HOST` default 127.0.0.1
- `REDIS_AUTH_PORT` default 6379
- `REDIS_AUTH_PASSWORD` default None
- `REDIS_AUTH_TOKEN_STORAGE` default 'headers' should be 'cookies'

## Define startapp and shutdown logic

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.gspot_fastapi_auth import token_config
from gspot_fastapi_auth.providers import RedisSingleton

@asynccontextmanager
async def lifespan(app: FastAPI):
    RedisSingleton.init_redis(
        token_config.HOST,
        token_config.PORT,
        token_config.DB,
        token_config.PASSWORD
    )
    yield
    await RedisSingleton().close()


app = FastAPI(lifespan=lifespan)

```

## Use in view
```python
from gspot_fastapi_auth import UserRedisAuth

@app.get("/")
async def read_root(user=Depends(UserRedisAuth())):
    return user.to_dict()

```
