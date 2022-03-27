from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.sql.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
