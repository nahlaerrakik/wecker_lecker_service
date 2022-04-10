from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.menu import query_menu
from app.crud.order import insert_order
from app.crud.order import insert_order_item_bulk
from app.enums.menu_type import MenuType
from app.enums.order_status import OrderStatus
from app.models.order import Order
from app.models.order import OrderItem as OrderItemModel
from app.schemas.order import OrderCreate
from app.schemas.order import OrderItem
from app.utils.exceptions import raise_invalid_menu_type_exception
from app.utils.exceptions import raise_invalid_order_status_exception
from app.utils.exceptions import raise_menu_id_not_found_exception


def validate_order_status(order_status: str) -> None:
    if OrderStatus.from_string(order_status) == OrderStatus.UNKNOWN:
        raise raise_invalid_order_status_exception(order_status=order_status)


def validate_menu_type(order_items: List[OrderItem]) -> None:
    for item in order_items:
        if MenuType.from_string(item.menu_type) == MenuType.UNKNOWN:
            raise_invalid_menu_type_exception(menu_type=item.menu_type)


def validate_menu_id(order_items: List[OrderItem], db: Session) -> None:
    for item in order_items:
        if not query_menu(db=db, menu_id=item.menu_id):
            raise_menu_id_not_found_exception(menu_id=item.menu_id)


def add_order(order: OrderCreate, db: Session) -> Order:
    try:
        order_db = insert_order(db, order=order)
        order_item_list = [OrderItemModel(
            quantity=item.quantity,
            price=item.price,
            menu_type=item.menu_type,
            menu_id=item.menu_id,
            order_id=order_db.id,
        ) for item in order.order_items]

        insert_order_item_bulk(db=db, order_item_list=order_item_list)
        db.commit()

        return order_db
    except IntegrityError as exc:
        db.rollback()
        raise exc
