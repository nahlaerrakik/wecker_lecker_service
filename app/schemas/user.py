from typing import Optional

from pydantic import BaseModel


class UserGet(BaseModel):
    email: str
    first_name: str
    last_name: str
    created_on: Optional[int] = None
    updated_on: Optional[int] = None
    is_active: Optional[bool] = None


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str


class UserUpdate(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
