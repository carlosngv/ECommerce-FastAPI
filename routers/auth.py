from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession


from models import UserTable
from schemas import User, UserCreate, Token
from config.database import get_db
from utils.jwt_manager import create_access_token, decode_token

auth_router = APIRouter(prefix='/auth', tags=['auth'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth')
# ? tokeUrl='token' referes to this path -> /token in the API

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
        # ? The "sub" can be named differently, is not a standard
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

@auth_router.post('/')
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

@auth_router.post('/registration')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await UserTable.create(db, **user.__dict__)
    # ? **user.__dict__, unpacks the dictionary representation of the UserCreate schema and spreads its "key:values"
    if not new_user:
        return JSONResponse(status_code=401, content={'msg': 'User was not created'})
    return JSONResponse(status_code=201, content={'msg': 'User created successfully'})
