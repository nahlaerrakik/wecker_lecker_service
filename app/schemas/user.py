from pydantic import BaseModel


class UserGet(BaseModel):
    email: str
    first_name: str
    last_name: str
    created_on: int
    updated_on: int


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str


