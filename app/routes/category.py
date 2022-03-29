from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.category import insert_category, query_category
from app.crud.category import query_categories
from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryGet
from app.sql.database import Base
from app.sql.database import engine
from app.sql.database import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/categories", response_model=CategoryGet, tags=["Categories"])
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    result = insert_category(db, category=category)

    return CategoryGet(
        id=result.id,
        name=result.name,
    )


@router.get("/categories", response_model=List[CategoryGet], tags=["Categories"])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = query_categories(db=db, skip=skip, limit=limit)

    return [CategoryGet(id=item.id, name=item.name) for item in result]


@router.get("/categories/{category_id}", response_model=CategoryGet, tags=["Categories"])
def get_category(category_id: int, db: Session = Depends(get_db)):
    result = query_category(db=db, category_id=category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return CategoryGet(
        id=result.id,
        name=result.name,
    )
