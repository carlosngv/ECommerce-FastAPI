from typing import Annotated

from models import UserTable
from schemas import UserUpdate
from config.database import get_db
from .auth import get_current_verified_user

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(prefix='/users', tags=['user'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth')

@user_router.put('/activate/{id}')
async def activate_user(id: str, db: AsyncSession = Depends(get_db)):
    user_activation_status = await UserTable.activate(db, id)
    if not user_activation_status:
        return JSONResponse(status_code=201, content={'msg': 'User already active'})
    return JSONResponse(status_code=201, content={'msg': 'User activated successfully'})

@user_router.put('/{id}')
async def update_user(current_user: Annotated[bool, Depends(get_current_verified_user)], id: str, user: UserUpdate,db: AsyncSession = Depends(get_db)):
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
async def get_all_users(current_user: Annotated[bool, Depends(get_current_verified_user)], db: AsyncSession = Depends(get_db)):
    users = await UserTable.get_all(db)
    if not users:
        return JSONResponse(status_code=401, content={'msg': 'There are no users registered'})
    return JSONResponse(status_code=200, content={'users': jsonable_encoder(users)})
