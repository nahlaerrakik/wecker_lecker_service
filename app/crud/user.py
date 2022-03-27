from typing import List

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


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


def query_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def query_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
