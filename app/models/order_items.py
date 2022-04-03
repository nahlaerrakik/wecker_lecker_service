from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app.data_access.database import Base
from app.enums.menu_type import MenuType


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    menu_type = Column(Enum(MenuType), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"))
