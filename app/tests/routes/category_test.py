import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import api
from app.models.catgeory import Category
from app.sql.database import Base
from app.sql.database import get_db

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


@pytest.fixture()
def client(session):
    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    api.dependency_overrides[get_db] = override_get_db

    yield TestClient(api)


def test_create_category(client, mocker):
    mocked_category = Category(id=1, name="category1")
    mocker.patch('app.routes.category.insert_category', return_value=mocked_category)

    response = client.post("/categories", json={"name": "category1"})
    assert response.status_code == 200

    result = response.json()
    assert result.get("id") == mocked_category.id
    assert result.get("name") == mocked_category.name


def test_get_categories_multiple_result(client, mocker):
    mocked_category_list = [
        Category(id=1, name="category1"),
        Category(id=2, name="category2"),
    ]
    mocker.patch('app.routes.category.query_categories', return_value=mocked_category_list)

    response = client.get("/categories")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2
    assert result == [
        dict(id=1, name="category1"),
        dict(id=2, name="category2"),
    ]


def test_get_categories_empty_result(client, mocker):
    mocker.patch('app.routes.category.query_categories', return_value=[])

    response = client.get("/categories")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0
    assert result == []


def test_get_category(client, mocker):
    mocked_category = Category(id=1, name="category1")
    mocker.patch('app.routes.category.query_category', return_value=mocked_category)

    response = client.get("/categories/1")
    assert response.status_code == 200

    result = response.json()
    assert result == dict(id=1, name="category1")


def test_get_category_not_found(client, mocker):
    mocker.patch('app.routes.category.query_category', return_value=None)

    response = client.get("/categories/1")
    assert response.status_code == 404

    result = response.json()
    assert result == {"detail": "Category not found"}
