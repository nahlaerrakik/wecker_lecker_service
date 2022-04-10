from typing import Optional, List

from sqlalchemy.orm import Session

from app.enums.order_status import OrderStatus
from app.models.order import Order
from app.models.order import OrderItem
from app.schemas.order import OrderCreate
from app.schemas.order import OrderUpdate
from app.utils.timestamp import CURRENT_TIMESTAMP


def insert_order(db: Session, order: OrderCreate) -> Order:
    item = Order(
        status=OrderStatus.PLACED,
        user_id=order.user_id,
    )

    db.add(item)
    db.flush()
    db.refresh(item)

    return item


def query_order(db: Session, order_id: int) -> Order:
    return db.query(Order).filter(Order.id == order_id).first()


def query_orders(db: Session) -> List[Order]:
    return db.query(Order).filter().all()


def update_order(db: Session, order: OrderUpdate) -> Optional[Order]:
    order_db = query_order(db, order_id=order.id)
    if order_db is None:
        return

    order_db.status = OrderStatus.from_string(order.status)
    order_db.updated_on = CURRENT_TIMESTAMP

    db.add(order_db)
    db.commit()
    db.refresh(order_db)

    return order_db


def insert_order_item_bulk(db: Session, order_item_list: List[OrderItem]) -> None:
    db.add_all(order_item_list)


def query_order_items(db: Session) -> List[OrderItem]:
    return db.query(OrderItem).filter().all()


def query_order_details(db: Session, order_id: int):
    return db.query(Order, OrderItem).join(OrderItem).filter(Order.id == order_id).all()

