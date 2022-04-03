from unittest import mock

import pytest

from app.crud.order import insert_order
from app.crud.order import query_order
from app.crud.order import update_order
from app.crud.user import insert_user
from app.enums.order_status import OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate
from app.schemas.user import UserCreate


@pytest.fixture
def mock_user_id(session):
    user = UserCreate(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )

    return insert_user(db=session, user=user).email


@pytest.fixture
def mock_order(session, mock_user_id):
    order = OrderCreate(
        user_id=mock_user_id,
    )

    return insert_order(db=session, order=order)


def test_insert_order(session, mock_user_id):
    order = OrderCreate(
        user_id=mock_user_id,
    )

    result = insert_order(db=session, order=order)
    assert result.status == OrderStatus.PLACED
    assert result.created_on == mock.ANY
    assert result.updated_on == mock.ANY
    assert result.user_id == mock_user_id


def test_query_order_with_existent_order_id(session, mock_order):
    result = query_order(db=session, order_id=mock_order.id)
    assert result == mock_order


def test_query_order_with_non_existent_order_id(session):
    result = query_order(db=session, order_id=-1)
    assert result is None


def test_update_order(session, mock_order):
    order_update = OrderUpdate(id=mock_order.id, status=OrderStatus.DELIVERED.value)
    result = update_order(db=session, order=order_update)

    assert result.id == mock_order.id
    assert result.status == OrderStatus.DELIVERED
    assert result.created_on == mock_order.created_on
    assert result.updated_on == mock.ANY
    assert result.user_id == mock_order.user_id
