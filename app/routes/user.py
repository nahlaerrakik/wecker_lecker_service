from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.user import insert_user
from app.crud.user import query_user
from app.schemas.user import UserCreate
from app.schemas.user import UserGet
from app.sql.database import Base
from app.sql.database import engine
from app.sql.database import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/users", response_model=UserGet, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = query_user(db, email=user.email)
    if user is not None:
        raise HTTPException(status_code=400, detail=f"User {user.email} already exists", )

    result = insert_user(db, user=user)

    return UserGet(
        email=result.email,
        first_name=result.first_name,
        last_name=result.last_name,
        created_on=result.created_on,
        updated_on=result.updated_on,
    )
