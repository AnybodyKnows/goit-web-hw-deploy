
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password:  str = Field(min_length=4, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    avatar: str
    model_config = ConfigDict(from_atributes=True)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
