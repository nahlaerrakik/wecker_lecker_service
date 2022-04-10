from pydantic import BaseModel


class MenuGet(BaseModel):
    id: int
    name: str
    short_description: str
    full_description: str
    price: float
    image: str
    category_id: int


class MenuCreate(BaseModel):
    name: str
    short_description: str
    full_description: str
    price: float
    image: str
    category_id: int
