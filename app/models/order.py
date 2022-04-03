from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func

from app.data_access.database import Base
from app.enums.order_status import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(Enum(OrderStatus), nullable=False)
    created_on = Column(Integer, nullable=False, default=func.current_timestamp())
    updated_on = Column(Integer, nullable=False, default=func.current_timestamp())
    user_id = Column(String, ForeignKey("users.email"))
