from typing import List

from sqlalchemy.orm import Session

from app.models.catgeory import Category
from app.schemas.category import CategoryCreate


def insert_category(db: Session, category: CategoryCreate) -> Category:
    item = Category(name=category.name)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def query_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def query_category(db: Session, category_id: int) -> Category:
    return db.query(Category).filter(Category.id == category_id).first()
