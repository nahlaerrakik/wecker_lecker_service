from datetime import timedelta

import pytest
from fastapi import HTTPException

from app.logic.user import authenticate_user, get_current_active_user
from app.logic.user import create_access_token
from app.logic.user import get_current_user
from app.logic.user import get_password_hash
from app.logic.user import pwd_context
from app.logic.user import verify_password
from app.models.user import User
from app.schemas.user import UserGet


def test_verify_password_success():
    plain_password = "test"
    hashed_password = pwd_context.hash(plain_password)

    assert verify_password(plain_password=plain_password, hashed_password=hashed_password) is True


def test_verify_password_failure():
    plain_password = "test"
    hashed_password = pwd_context.hash("hash_test")

    assert verify_password(plain_password=plain_password, hashed_password=hashed_password) is False


def test_get_password_hash(mocker):
    mocker.patch('app.logic.user.pwd_context.hash', return_value="qwerty")

    assert get_password_hash(password="test") == "qwerty"


def test_authenticate_user(session, mocker):
    user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )
    mocker.patch('app.logic.user.query_user', return_value=user)
    mocker.patch('app.logic.user.verify_password', return_value=True)

    assert authenticate_user(db=session, email="joe@doe.com", password="joedoe") == user


def test_authenticate_user_with_non_existent_user(session, mocker):
    mocker.patch('app.logic.user.query_user', return_value=None)

    assert authenticate_user(db=session, email="joe@doe.com", password="joedoe") is False


def test_authenticate_user_with_non_matching_password(session, mocker):
    user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )
    mocker.patch('app.logic.user.query_user', return_value=user)
    mocker.patch('app.logic.user.verify_password', return_value=False)

    assert authenticate_user(db=session, email="joe@doe.com", password="joedoe") is False


def test_create_access_token_with_expires_delta(mocker):
    mocker.patch('app.logic.user.jwt.encode', return_value="token_with_expires_delta")
    data = {"sub": "data"}

    assert create_access_token(data=data, expires_delta=timedelta(minutes=100)) == "token_with_expires_delta"


@pytest.mark.asyncio
async def test_get_current_user(mocker):
    user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )
    mocker.patch('app.logic.user.jwt.decode', return_value=dict(sub=user.email))
    mocker.patch('app.logic.user.query_user', return_value=user)

    assert await get_current_user(token="token") == user


@pytest.mark.asyncio
async def test_get_current_user_with_empty_payload(mocker):
    mocker.patch('app.logic.user.jwt.decode', return_value=dict())

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="token")

    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
async def test_get_current_user_with_non_existent_user(mocker):
    mocker.patch('app.logic.user.jwt.decode', return_value=dict(sub="joe@doe.com"))
    mocker.patch('app.logic.user.query_user', return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="token")

    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(mocker):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="token")

    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
async def test_get_current_active_user_enabled():
    user = UserGet(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        created_on=1,
        updated_on=1,
    )

    assert await get_current_active_user(current_user=user) == user


@pytest.mark.asyncio
async def test_get_current_active_user_disabled():
    user = UserGet(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        created_on=1,
        updated_on=1,
        is_active=True,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_active_user(current_user=user)

    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Inactive user"
