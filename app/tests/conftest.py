import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import api
from app.sql.database import Base
from app.sql.database import get_db

SQLALCHEMY_DATABASE_URL = r"sqlite:///D:\\wecker_lecker_service\\app\\sql\\test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def client(session):
    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    api.dependency_overrides[get_db] = override_get_db

    yield TestClient(api)
