from unittest import mock

import pytest

from app.crud.category import insert_category
from app.crud.menu import insert_menu
from app.crud.order import insert_order, query_order_items
from app.crud.order import insert_order_item_bulk
from app.crud.order import query_order_details
from app.crud.order import query_order
from app.crud.order import update_order
from app.crud.user import insert_user
from app.enums.order_status import OrderStatus
from app.schemas.category import CategoryCreate
from app.schemas.menu import MenuCreate
from app.schemas.order import OrderCreate
from app.models.order import OrderItem
from app.schemas.order import OrderUpdate
from app.schemas.user import UserCreate


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
def mock_order(session, mock_user):
    order = OrderCreate(
        user_id=mock_user.email,
    )

    return insert_order(db=session, order=order)


@pytest.fixture()
def mock_menu(session):
    category = CategoryCreate(
        name="category",
    )
    category_id = insert_category(db=session, category=category).id

    menu = MenuCreate(
        name="menu",
        short_description="short_description",
        full_description="full_description",
        price=1.0,
        image="image",
        category_id=category_id
    )
    return insert_menu(db=session, menu=menu)


@pytest.fixture
def mock_order_items(session, mock_order, mock_menu):
    return [
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="FRESH",
            menu_id=mock_menu.id,
            order_id=mock_order.id,
        ),
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="COOKED",
            menu_id=mock_menu.id,
            order_id=mock_order.id,
        )
    ]


def test_insert_order(session, mock_user):
    order = OrderCreate(
        user_id=mock_user.email,
    )

    result = insert_order(db=session, order=order)
    assert result.status == OrderStatus.PLACED
    assert result.created_on == mock.ANY
    assert result.updated_on == mock.ANY
    assert result.user_id == mock_user.email


def test_query_order_with_existent_order_id(session, mock_order):
    session.commit()
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


def test_update_order_with_non_existent(session):
    order_update = OrderUpdate(id=-1, status=OrderStatus.DELIVERED.value)
    result = update_order(db=session, order=order_update)
    assert result is None


def test_insert_order_item_bulk(session, mock_order, mock_menu, mock_order_items):
    assert insert_order_item_bulk(db=session, order_item_list=mock_order_items) is None
    assert query_order_items(session) == []

    session.commit()
    assert query_order_items(session) == mock_order_items


def test_query_order_details(session, mock_order, mock_menu, mock_order_items):
    insert_order_item_bulk(session, order_item_list=mock_order_items)
    session.commit()

    result = query_order_details(db=session, order_id=mock_order.id)
    assert len(result) == 2

    order_item = result[0]
    assert order_item.OrderItem.quantity == mock_order_items[0].quantity
    assert order_item.OrderItem.price == mock_order_items[0].price
    assert order_item.OrderItem.menu_type == mock_order_items[0].menu_type
    assert order_item.OrderItem.menu_id == mock_order_items[0].menu_id
    assert order_item.OrderItem.order_id == mock_order.id

    order_item = result[1]
    assert order_item.OrderItem.quantity == mock_order_items[1].quantity
    assert order_item.OrderItem.price == mock_order_items[1].price
    assert order_item.OrderItem.menu_type == mock_order_items[1].menu_type
    assert order_item.OrderItem.menu_id == mock_order_items[1].menu_id
    assert order_item.OrderItem.order_id == mock_order.id


def test_query_order_details_empty(session):
    result = query_order_details(db=session, order_id=-1)
    assert result == []
