from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums.menu_type import MenuType
from app.enums.order_status import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(Enum(OrderStatus), nullable=False)
    created_on = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_on = Column(DateTime, nullable=False, default=func.current_timestamp())
    user_id = Column(String, ForeignKey("users.email"))

    order_items = relationship("OrderItem", backref="orders")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    menu_type = Column(Enum(MenuType), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
