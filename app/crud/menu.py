from typing import List

from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.schemas.menu import MenuCreate


def insert_menu(db: Session, menu: MenuCreate) -> Menu:
    item = Menu(
        name=menu.name,
        short_description=menu.short_description,
        full_description=menu.full_description,
        price=menu.price,
        image=menu.image,
        category_id=menu.category_id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def query_menus(db: Session, skip: int = 0, limit: int = 100) -> List[Menu]:
    return db.query(Menu).offset(skip).limit(limit).all()


def query_menu(db: Session, menu_id: int) -> Menu:
    return db.query(Menu).filter(Menu.id == menu_id).first()


def query_menus_by_category(db: Session, category_id: int) -> List[Menu]:
    return db.query(Menu).filter(Menu.category_id == category_id).all()
