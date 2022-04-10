from typing import List
from typing import Optional

from pydantic import BaseModel


class OrderItem(BaseModel):
    quantity: int
    price: float
    menu_type: str
    menu_id: int


class OrderGet(BaseModel):
    id: int
    status: str
    created_on: Optional[int] = None
    updated_on: Optional[int] = None
    user_id: str


class OrderCreate(BaseModel):
    user_id: str
    order_items: Optional[List[OrderItem]] = None


class OrderUpdate(BaseModel):
    id: int
    status: str

