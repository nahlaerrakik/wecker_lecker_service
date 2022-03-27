import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import api
from app.models.user import User
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


def test_create_user(client, mocker):
    ts = int(time.time())

    mocked_user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
        created_on=ts,
        updated_on=ts,
    )
    mocker.patch('app.routes.user.insert_user', return_value=mocked_user)

    response = client.post(
        url="/users",
        json={
            "email": "joe@doe.com",
            "first_name": "joe",
            "last_name": "doe",
            "password": "joedoe",
        }
    )
    assert response.status_code == 200

    result = response.json()
    assert result.get("email") == mocked_user.email
    assert result.get("first_name") == mocked_user.first_name
    assert result.get("last_name") == mocked_user.last_name
    assert result.get("created_on") == mocked_user.created_on
    assert result.get("updated_on") == mocked_user.updated_on


def test_create_user_already_exist(client, mocker):
    ts = int(time.time())

    mocked_existent_user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
        created_on=ts,
        updated_on=ts,
    )
    mocker.patch('app.routes.user.query_user', return_value=mocked_existent_user)

    response = client.post(
        url="/users",
        json={
            "email": "joe@doe.com",
            "first_name": "joe",
            "last_name": "doe",
            "password": "joedoe",
        }
    )
    assert response.status_code == 400

    result = response.json()
    assert result == {"detail": "User joe@doe.com already exists"}
