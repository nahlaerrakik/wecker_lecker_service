from unittest import mock

import pytest
import pytest_mock.plugin

from app.crud.user import insert_user
from app.crud.user import update_user
from app.crud.user import query_user
from app.crud.user import query_users
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate


@pytest.fixture
def mock_user(session):
    user = UserCreate(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )

    return insert_user(db=session, user=user)


@pytest.fixture
def mock_user_list(session):
    user1 = insert_user(
        db=session,
        user=UserCreate(email="joe@doe.com", first_name="joe", last_name="doe", password="joedoe", )
    )
    user2 = insert_user(
        db=session,
        user=UserCreate(email="jane@doe.com", first_name="jane", last_name="doe", password="janedoe", )
    )

    return [user1, user2]


def test_insert_user(session):
    user1 = UserCreate(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )

    result = insert_user(db=session, user=user1)
    assert result.email == user1.email
    assert result.first_name == user1.first_name.capitalize()
    assert result.last_name == user1.last_name.upper()
    assert result.password == user1.password
    assert result.created_on == mock.ANY
    assert result.updated_on == mock.ANY
    assert result.is_active is False

    user2 = UserCreate(
        email="jane@doe.com",
        first_name="jane",
        last_name="doe",
        password="janedoe",
    )
    result = insert_user(db=session, user=user2)
    assert result.email == user2.email
    assert result.first_name == user2.first_name.capitalize()
    assert result.last_name == user2.last_name.upper()
    assert result.password == user2.password
    assert result.created_on == mock.ANY
    assert result.updated_on == mock.ANY
    assert result.is_active is False


def test_query_users_multiple_result(session, mock_user_list):
    result = query_users(db=session)
    assert len(result) == len(mock_user_list)
    assert result == mock_user_list


def test_query_users_empty_result(session):
    result = query_users(db=session)
    assert len(result) == 0
    assert result == []

    result = query_users(db=session, skip=1)
    assert len(result) == 0
    assert result == []

    result = query_users(db=session, limit=1)
    assert len(result) == 0
    assert result == []

    result = query_users(db=session, skip=1, limit=1)
    assert len(result) == 0
    assert result == []


def test_query_user_non_existent_user(session):
    result = query_user(db=session, email="notfound@email.com")
    assert result is None


def test_update_user_first_name(session, mock_user):
    user_update = UserUpdate(email=mock_user.email, first_name="test")
    result = update_user(db=session, user=user_update)

    assert result.email == mock_user.email
    assert result.first_name == "Test"
    assert result.last_name == mock_user.last_name.upper()
    assert result.password == mock_user.password
    assert result.created_on == mock_user.created_on
    assert result.updated_on == mock.ANY
    assert result.is_active is False


def test_update_user_last_name(session, mock_user):
    user_update = UserUpdate(email=mock_user.email, last_name="test")
    result = update_user(db=session, user=user_update)

    assert result.email == mock_user.email
    assert result.first_name == mock_user.first_name.capitalize()
    assert result.last_name == "TEST"
    assert result.password == mock_user.password
    assert result.created_on == mock_user.created_on
    assert result.updated_on == mock.ANY
    assert result.is_active is False


def test_update_user_password(session, mock_user):
    user_update = UserUpdate(email=mock_user.email, password="test")
    result = update_user(db=session, user=user_update)

    assert result.email == mock_user.email
    assert result.first_name == mock_user.first_name.capitalize()
    assert result.last_name == mock_user.last_name.upper()
    assert result.password == "test"
    assert result.created_on == mock_user.created_on
    assert result.updated_on == mock.ANY
    assert result.is_active is False


def test_update_user_is_active(session, mock_user):
    user_update = UserUpdate(email=mock_user.email, is_active=True)
    result = update_user(db=session, user=user_update)

    assert result.email == mock_user.email
    assert result.first_name == mock_user.first_name.capitalize()
    assert result.last_name == mock_user.last_name.upper()
    assert result.password == mock_user.password
    assert result.created_on == mock_user.created_on
    assert result.updated_on == mock.ANY
    assert result.is_active is True


def test_update_user_with_non_existent_user(session):
    user_update = UserUpdate(email="joe@doe.com")
    assert update_user(db=session, user=user_update) is None
