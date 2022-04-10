import pytest
from fastapi import HTTPException

from app.enums.menu_type import MenuType
from app.enums.order_status import OrderStatus
from app.utils.exceptions import raise_invalid_menu_type_exception
from app.utils.exceptions import raise_invalid_order_status_exception
from app.utils.exceptions import raise_menu_id_not_found_exception


def test_raise_invalid_order_status_exception():
    with pytest.raises(HTTPException) as exc:
        raise_invalid_order_status_exception(order_status="TEST")

    assert exc.value.status_code == 400
    assert exc.value.detail == f"Invalid order_status TEST, should be one of the following values {OrderStatus.list_values()}."


def test_raise_invalid_menu_type_exception():
    with pytest.raises(HTTPException) as exc:
        raise_invalid_menu_type_exception(menu_type="TEST")

    assert exc.value.status_code == 400
    assert exc.value.detail == f"Invalid menu_type TEST, should be one of the following values {MenuType.list_values()}."


def test_raise_menu_id_not_found_exception():
    with pytest.raises(HTTPException) as exc:
        raise_menu_id_not_found_exception(menu_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == f"Menu with id {1} does not exist."
