from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    short_description = Column(String)
    full_description = Column(String)
    price = Column(Float)
    image = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
