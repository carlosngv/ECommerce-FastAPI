from typing import List
from schemas import User
from models import UserTable

from fastapi import APIRouter, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import sessionmanager, get_db

user_router = APIRouter(prefix='/users', tags=['user'])

@user_router.get('/', response_model=List[User])
async def get_users(db: AsyncSession = Depends(get_db)):
    # users = await User.get_all(db)
    result = await db.execute(select(UserTable))
    users = result.scalars().all()
    return JSONResponse(status_code=200, content={'users': jsonable_encoder(users)})
