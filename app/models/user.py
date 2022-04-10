from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    created_on = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_on = Column(DateTime, nullable=False, default=func.current_timestamp())
    is_active = Column(Boolean, nullable=False, default=False)

    orders = relationship("Order")
