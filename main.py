
import sys
import uvicorn
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.database import sessionmanager, create_tables
from routers.users import user_router

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

fake_users = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ? Runs one time
    await create_tables()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan, title='ECommerceAPI', docs_url='/api/docs')



app.include_router(user_router, prefix='/api', tags=['user'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
