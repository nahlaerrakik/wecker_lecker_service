from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud.user import insert_user, update_user
from app.crud.user import query_user
from app.exceptions import INVALID_CREDENTIALS_EXCEPTION
from app.logic.user import ACCESS_TOKEN_EXPIRE_MINUTES
from app.logic.user import authenticate_user
from app.logic.user import create_access_token
from app.logic.user import get_current_active_user
from app.logic.user import get_password_hash
from app.schemas.user import UserCreate
from app.schemas.user import Token
from app.schemas.user import UserUpdate
from app.schemas.user import UserGet
from app.sql.database import Base
from app.sql.database import engine
from app.sql.database import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/users", response_model=UserGet, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if query_user(db, email=user.email) is not None:
        raise HTTPException(status_code=400, detail=f"User {user.email} already exists", )

    user.password = get_password_hash(password=user.password)
    result = insert_user(db, user=user)

    return UserGet(
        email=result.email,
        first_name=result.first_name,
        last_name=result.last_name,
    )


@router.post("/token", response_model=Token, tags=["Users"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise INVALID_CREDENTIALS_EXCEPTION

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    update_user(db, user=UserUpdate(email=user.email, is_active=True))

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/users/me", response_model=UserGet, tags=["Users"])
async def read_users_me(current_user: UserGet = Depends(get_current_active_user)):
    return current_user
