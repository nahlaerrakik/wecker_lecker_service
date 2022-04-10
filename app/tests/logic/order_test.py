from unittest import mock

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.crud.category import insert_category
from app.crud.menu import insert_menu
from app.crud.order import query_orders
from app.crud.order import query_order_details
from app.crud.order import query_order_items
from app.crud.user import insert_user
from app.enums.menu_type import MenuType
from app.enums.order_status import OrderStatus
from app.logic.order import add_order
from app.logic.order import validate_menu_id
from app.logic.order import validate_menu_type
from app.logic.order import validate_order_status
from app.schemas.category import CategoryCreate
from app.schemas.menu import MenuCreate
from app.schemas.order import OrderItem, OrderCreate
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
def mock_order_setup(session):
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
    menu_id = insert_menu(db=session, menu=menu).id

    return {
        "category_id": category_id,
        "menu_id": menu_id,
    }


def test_validate_order_status_with_valid_value():
    assert validate_order_status(order_status="PLACED") is None


def test_validate_order_status_with_invalid_value():
    with pytest.raises(HTTPException) as exc:
        validate_order_status(order_status="TEST")

    assert exc.value.status_code == 400
    assert exc.value.detail == f"Invalid order_status TEST, should be one of the following values {OrderStatus.list_values()}."


def test_validate_menu_type_with_valid_value(session):
    order_items = [
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="FRESH",
            menu_id=1,
        )
    ]
    assert validate_menu_type(order_items=order_items) is None


def test_validate_menu_type_with_invalid_value():
    order_items = [
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="FRESH",
            menu_id=1,
        ),
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="TEST",
            menu_id=1,
        )
    ]

    with pytest.raises(HTTPException) as exc:
        validate_menu_type(order_items=order_items)

    assert exc.value.status_code == 400
    assert exc.value.detail == f"Invalid menu_type TEST, should be one of the following values {MenuType.list_values()}."


def test_validate_menu_id_with_existing_value(session, mocker):
    mocker.patch('app.logic.order.query_menu', return_value=mock.ANY)
    order_items = [
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="FRESH",
            menu_id=1,
        ),
    ]
    assert validate_menu_id(order_items=order_items, db=session) is None


def test_validate_menu_id_with_non_existing_value(session, mocker):
    mocker.patch('app.logic.order.query_menu', return_value=None)
    order_items = [
        OrderItem(
            quantity=1,
            price=1.0,
            menu_type="FRESH",
            menu_id=1,
        ),
    ]
    with pytest.raises(HTTPException) as exc:
        validate_menu_id(order_items=order_items, db=session)

    assert exc.value.status_code == 404
    assert exc.value.detail == f"Menu with id {1} does not exist."


def test_add_order(session, mock_user, mock_order_setup):
    order_create = OrderCreate(
        user_id=mock_user.email,
        order_items=[
            OrderItem(
                quantity=1,
                price=1.0,
                menu_type="FRESH",
                menu_id=mock_order_setup["menu_id"],
            )
        ]
    )

    result = add_order(order=order_create, db=session)
    assert result.status == OrderStatus.PLACED
    assert result.user_id == mock_user.email

    order_detail = query_order_details(db=session, order_id=result.id)[0]
    assert order_detail.Order == result
    assert order_detail.OrderItem.quantity == 1
    assert order_detail.OrderItem.menu_type == MenuType.FRESH
    assert order_detail.OrderItem.menu_id == mock_order_setup["menu_id"]
    assert order_detail.OrderItem.order_id == result.id


def test_add_order_with_exception(session, mock_user):
    order_create = OrderCreate(
        user_id=mock_user.email,
        order_items=[
            OrderItem(
                quantity=1,
                price=1.0,
                menu_type="FRESH",
                menu_id=-1,
            )
        ]
    )

    with pytest.raises(IntegrityError):
        add_order(order=order_create, db=session)

    assert query_orders(db=session) == []
    assert query_order_items(db=session) == []



