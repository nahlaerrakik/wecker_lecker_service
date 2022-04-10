from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.category import query_category
from app.crud.menu import insert_menu
from app.crud.menu import query_menu
from app.crud.menu import query_menus
from app.crud.menu import query_menus_by_category
from app.database import get_db
from app.schemas.menu import MenuCreate
from app.schemas.menu import MenuGet

router = APIRouter()


@router.post("/api/v1/menus", response_model=MenuGet, tags=["Menus"], status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    category = query_category(db, category_id=menu.category_id)
    if category is None:
        raise HTTPException(status_code=400, detail=f"Invalid request. Category with id {menu.category_id} not found", )

    result = insert_menu(db, menu=menu)

    return MenuGet(
        id=result.id,
        name=result.name,
        short_description=result.short_description,
        full_description=result.full_description,
        price=result.price,
        image=result.image,
        category_id=result.category_id,
    )


@router.get("/api/v1/menus", response_model=List[MenuGet], tags=["Menus"])
def get_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = query_menus(db=db, skip=skip, limit=limit)

    return [
        MenuGet(
            id=item.id,
            name=item.name,
            short_description=item.short_description,
            full_description=item.full_description,
            price=item.price,
            image=item.image,
            category_id=item.category_id,
        ) for item in result
    ]


@router.get("/api/v1/menus/{menu_id}", response_model=MenuGet, tags=["Menus"])
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    result = query_menu(db=db, menu_id=menu_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Menu with {menu_id} not found")

    return MenuGet(
        id=result.id,
        name=result.name,
        short_description=result.short_description,
        full_description=result.full_description,
        price=result.price,
        image=result.image,
        category_id=result.category_id,
    )


@router.get("/api/v1/search/menus", response_model=List[MenuGet], tags=["Menus"])
def search_menus_by_category(category_id: int, db: Session = Depends(get_db)):
    result = query_menus_by_category(db=db, category_id=category_id)

    return [
        MenuGet(
            id=item.id,
            name=item.name,
            short_description=item.short_description,
            full_description=item.full_description,
            price=item.price,
            image=item.image,
            category_id=item.category_id,
        ) for item in result
    ]