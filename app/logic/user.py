from datetime import datetime
from datetime import timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.crud.user import query_user
from app.utils.exceptions import INVALID_CREDENTIALS_EXCEPTION
from app.utils.exceptions import INACTIVE_USER_EXCEPTION
from app.models.user import User
from app.schemas.user import TokenData
from app.schemas.user import UserGet
from app.data_access.database import get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    user = query_user(db, email)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        if username is None:
            raise INVALID_CREDENTIALS_EXCEPTION

        token_data = TokenData(username=username)
    except JWTError:
        raise INVALID_CREDENTIALS_EXCEPTION

    user = query_user(db, email=token_data.username)
    if user is None:
        raise INVALID_CREDENTIALS_EXCEPTION

    return user


async def get_current_active_user(current_user: UserGet = Depends(get_current_user)):
    if current_user.is_active:
        raise INACTIVE_USER_EXCEPTION

    return current_user
