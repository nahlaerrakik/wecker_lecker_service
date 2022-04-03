from app.enums.order_status import OrderStatus


def test_order_status_from_string_valid_value():
    assert OrderStatus.from_string("PLACED") == OrderStatus.PLACED
    assert OrderStatus.from_string("PROCESSING") == OrderStatus.PROCESSING
    assert OrderStatus.from_string("DISPATCHED") == OrderStatus.DISPATCHED
    assert OrderStatus.from_string("DELIVERED") == OrderStatus.DELIVERED


def test_order_status_from_string_invalid_value():
    assert OrderStatus.from_string("TEST") == OrderStatus.UNKNOWN


def test_order_status_from_list_values():
    assert OrderStatus.list_values() == ["PLACED", "PROCESSING", "DISPATCHED", "DELIVERED"]

