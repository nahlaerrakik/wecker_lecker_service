from app.database import get_db
from app.database import SessionLocal


def test_get_db(session):
    expected = SessionLocal()
    result = next(get_db())

    assert result.autocommit == expected.autocommit
    assert result.autoflush == expected.autoflush
    assert result.bind == expected.bind
