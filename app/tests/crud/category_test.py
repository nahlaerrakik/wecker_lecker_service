from app.crud.category import insert_category
from app.crud.category import query_categories
from app.crud.category import query_category
from app.schemas.category import CategoryCreate


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
