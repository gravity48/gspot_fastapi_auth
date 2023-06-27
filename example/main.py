from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from src.gspot_fastapi_auth import UserRedisAuth, is_customer

from src.gspot_fastapi_auth import token_config
from src.gspot_fastapi_auth.providers import RedisSingleton


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


@app.get("/")
async def read_root(user=Depends(UserRedisAuth())):
    return user.to_dict()


@app.get("/customer/")
async def read_customer(user=Depends(is_customer)):
    return user.to_dict()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
