from datetime import timedelta
from typing import List, Annotated

from models import UserTable
from config.database import get_db
from schemas import User, UserCreate, UserUpdate, Token
from utils.jwt_manager import create_access_token, decode_token

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError


user_router = APIRouter(prefix='/users', tags=['user'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/token')
# ? tokeUrl='token' referes to this path -> /token in the API

@user_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)) -> Token:
    db_user = await UserTable.authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            # ? Header returned when requested protected resource but fail (is a standard header)
            headers={'WWW-Authenticate': 'Bearer'}
        )
    # ? Initial token duration (current time + 30 minutes)
    access_token_expires = timedelta(minutes=30)
    # ? Generate token
    access_token = create_access_token(data={'sub': form_data.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type='bearer') # ? The return Token must have this structure, and MUST return a JSON (standard)
    # return JSONResponse(status_code=200, content={'access_token': acces_token, 'token_type': 'bearer'})

@user_router.post('/registration')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await UserTable.create(db, **user.__dict__)
    # ? **user.__dict__, unpacks the dictionary representation of the UserCreate schema and spreads its "key:values"
    if not new_user:
        return JSONResponse(status_code=401, content={'msg': 'User was not created'})
    return JSONResponse(status_code=201, content={'msg': 'User created successfully'})


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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print('***** TOKEN ******* ', token)
        payload = decode_token(token)
        # ? Validates if token is expired
        if not payload:
            raise HTTPException(
                satus_code=301,
                detail='Your session has already expired',
                headers={"WWW-Authenticate": "Bearer"},
            )

        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        current_user = await UserTable.get_by_email(db, username)
        return current_user
    except InvalidTokenError as e:
        raise e

async def get_current_verified_user(current_user: Annotated[User, Depends(get_current_user)]) -> bool:
    if not current_user.is_verified:
        raise HTTPException(status_code=401, detail='Inactive user')
    return True


@user_router.get('/')
async def get_all_users(current_user: Annotated[bool, Depends(get_current_verified_user)], db: AsyncSession = Depends(get_db)):
    print(current_user)
    users = await UserTable.get_all(db)
    if not users:
        return JSONResponse(status_code=401, content={'msg': 'There are no users registered'})
    return JSONResponse(status_code=200, content={'users': jsonable_encoder(users)})
