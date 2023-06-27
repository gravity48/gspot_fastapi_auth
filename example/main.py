import uvicorn
from fastapi import FastAPI, Depends
from gspot_fastapi_auth import UserRedisAuth, is_customer

app = FastAPI()


@app.get("/")
async def read_root(user=Depends(UserRedisAuth())):
    return user.to_dict()


@app.get("/customer/")
async def read_customer(user=Depends(is_customer)):
    return user.to_dict()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
