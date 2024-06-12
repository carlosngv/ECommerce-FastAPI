import re
from typing import Optional, Annotated
from pydantic import (
    BaseModel,
    Field,
    field_validator
)

EMAIL_PATTERN = '[^@]+@[^@]+\.[^@]+'

class User(BaseModel):
    id: Optional[int] = None
    email: str = Field()
    password: Annotated[str, Field(min_length=8, max_length=20)]
    is_verified: bool = False
    join_data: str

    @field_validator('email')
    @classmethod
    def check_email(cls, value) -> str:
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError('Email value is not supported.')

        return value

class UserCreate(BaseModel):
    email: str = Field()
    password: Annotated[str, Field(min_length=8, max_length=20)]

    @field_validator('email')
    @classmethod
    def check_email(cls, value) -> str:
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError('Email value is not supported.')
        return value

class UserUpdate(BaseModel):
    email: str = Field()
    password: Optional[str] = ''

    @field_validator('email')
    @classmethod
    def check_email(cls, value) -> str:
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError('Email value is not supported.')
        return value
