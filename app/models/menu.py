from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.sql.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    image = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
