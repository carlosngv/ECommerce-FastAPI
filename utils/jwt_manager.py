import jwt
from typing import Union
from schemas import Token
from datetime import timedelta, datetime, timezone

SECRET_KEY = "b777ced068c79bb7ce8b7aba35a807346bc7abcc27b375ed25d8d0cff6390f54"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
