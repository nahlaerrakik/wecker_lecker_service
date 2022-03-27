import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.sql.database import Base
from app.crud.category import query_categories
from app.crud.category import query_category
from app.crud.category import insert_category
from app.schemas.category import CategoryCreate

SQLALCHEMY_DATABASE_URL = r"sqlite:///D:\\wecker_lecker_service\\app\\sql\\test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_insert_category(session):
    result = insert_category(db=session, category=CategoryCreate(name="category1"))
    assert result.id == 1
    assert result.name == "category1"

    result = insert_category(db=session, category=CategoryCreate(name="category2"))
    assert result.id == 2
    assert result.name == "category2"


def test_query_categories_multiple_result(session):
    category1 = insert_category(db=session, category=CategoryCreate(name="category1"))
    category2 = insert_category(db=session, category=CategoryCreate(name="category2"))
    category3 = insert_category(db=session, category=CategoryCreate(name="category2"))

    result = query_categories(db=session)
    assert len(result) == 3
    assert result == [category1, category2, category3]


def test_query_categories_empty_result(session):
    result = query_categories(db=session)
    assert len(result) == 0
    assert result == []

    result = query_categories(db=session, skip=1)
    assert len(result) == 0
    assert result == []

    result = query_categories(db=session, limit=1)
    assert len(result) == 0
    assert result == []

    result = query_categories(db=session, skip=1, limit=1)
    assert len(result) == 0
    assert result == []


def test_query_category(session):
    category = insert_category(db=session, category=CategoryCreate(name="category1"))

    result = query_category(db=session, category_id=category.id)
    assert result.id == category.id
    assert result.name == category.name


def test_query_category_non_existent_category(session):
    result = query_category(db=session, category_id=-1)
    assert result is None
