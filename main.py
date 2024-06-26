
import sys
import uvicorn
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.database import sessionmanager, create_tables
from routers import auth_router, user_router, business_router

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ? Runs one time
    await create_tables()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan, title='ECommerceAPI', docs_url='/api/docs')



app.include_router(auth_router, prefix='/api', tags=['auth'])
app.include_router(user_router, prefix='/api', tags=['user'])
app.include_router(business_router, prefix='/api', tags=['business'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
