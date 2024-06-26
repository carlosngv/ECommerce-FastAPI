import jwt
from typing import Union
from decouple import config
from datetime import timedelta, datetime, timezone

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload.update({'exp': expire}) # ? exp field is necessary to define expiration time inside the payload (token)
    # ? Always use a UTC timestamp or datetime in encoding
    encoded_jwt: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    return data
