from typing import List
from schemas import User, UserCreate, UserUpdate
from models import UserTable

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db

user_router = APIRouter(prefix='/users', tags=['user'])

@user_router.get('/', response_model=List[User])
async def get_users(db: AsyncSession = Depends(get_db)):
    # users = await User.get_all(db)
    result = await db.execute(select(UserTable))
    users = result.scalars().all()
    return JSONResponse(status_code=200, content={'users': jsonable_encoder(users)})

@user_router.post('/registration')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await UserTable.create(db, **user.__dict__)
    # ? **user.__dict__, unpacks the dictionary representation of the UserCreate schema
    if not new_user:
        return JSONResponse(status_code=401, content={'msg': 'User was not created'})
    return JSONResponse(status_code=201, content={'msg': 'User created successfully', 'user': jsonable_encoder(user)})


@user_router.put('/{id}')
async def update_user(id: str, user: UserUpdate,db: AsyncSession = Depends(get_db)):
    updated_user = await UserTable.update(db, id, **user.__dict__)
    if not updated_user:
        return JSONResponse(status_code=401, content={'msg': 'User was not updated'})
    return JSONResponse(status_code=201, content={'msg': 'User updated successfully'})


@user_router.get('/{id}')
async def get_user(id: str, db: AsyncSession = Depends(get_db)):
    user =  await UserTable.get(db, id)
    if not user:
        return JSONResponse(status_code=401, content={'msg': 'User does not exist'})
    return JSONResponse(status_code=200, content={'msg': 'User successfully found', 'user': jsonable_encoder(user)})

@user_router.get('/')
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await UserTable.get_all(db)
    if not users:
        return JSONResponse(status_code=401, content={'msg': 'There are no users registered'})
    return JSONResponse(status_code=200, content={'user': jsonable_encoder(users)})
