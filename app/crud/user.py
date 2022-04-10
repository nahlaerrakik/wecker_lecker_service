from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.utils.timestamp import CURRENT_TIMESTAMP


def insert_user(db: Session, user: UserCreate) -> User:
    item = User(
        email=user.email,
        first_name=user.first_name.capitalize(),
        last_name=user.last_name.upper(),
        password=user.password,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def update_user(db: Session, user: UserUpdate) -> Optional[User]:
    user_db = query_user(db, email=user.email)
    if user_db is None:
        return

    if user.first_name:
        user_db.first_name = user.first_name.capitalize()
    if user.last_name:
        user_db.last_name = user.last_name.upper()
    if user.password:
        user_db.password = user.password
    if user.is_active:
        user_db.is_active = user.is_active

    user_db.updated_on = CURRENT_TIMESTAMP

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


def query_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def query_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
