from typing import Optional

from pydantic import BaseModel


class OrderGet(BaseModel):
    id: int
    status: str
    created_on: Optional[int] = None
    updated_on: Optional[int] = None
    user_id: str


class OrderCreate(BaseModel):
    user_id: str


class OrderUpdate(BaseModel):
    id: int
    status: str
