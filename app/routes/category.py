from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.category import insert_category, query_category
from app.crud.category import query_categories
from app.database import get_db
from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryGet

router = APIRouter()


@router.post("/api/v1/categories", response_model=CategoryGet, tags=["Categories"], status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    result = insert_category(db, category=category)

    return CategoryGet(
        id=result.id,
        name=result.name,
    )


@router.get("/api/v1/categories", response_model=List[CategoryGet], tags=["Categories"])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = query_categories(db=db, skip=skip, limit=limit)

    return [CategoryGet(id=item.id, name=item.name) for item in result]


@router.get("/api/v1/categories/{category_id}", response_model=CategoryGet, tags=["Categories"])
def get_category(category_id: int, db: Session = Depends(get_db)):
    result = query_category(db=db, category_id=category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return CategoryGet(
        id=result.id,
        name=result.name,
    )
