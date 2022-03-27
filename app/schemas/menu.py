from pydantic import BaseModel


class MenuGet(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category_id: int


class MenuCreate(BaseModel):
    name: str
    description: str
    price: float
    image: str
    category_id: int
