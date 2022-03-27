from pydantic import BaseModel


class CategoryGet(BaseModel):
    id: int
    name: str


class CategoryCreate(BaseModel):
    name: str

