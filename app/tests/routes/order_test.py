import pytest

from app.enums.order_status import OrderStatus
from app.models.order import Order


@pytest.fixture
def mock_order():
    return Order(
        id=1,
        status=OrderStatus.PLACED,
        created_on=123456789,
        updated_on=123456789,
        user_id="joedoe@gmail.com",
    )


def test_create_order(client, mock_order, mocker):
    mocker.patch('app.routes.order.insert_order', return_value=mock_order)

    response = client.post(
        url="/orders",
        json={
            "user_id": "joedoe@gmail.com",
        }
    )
    assert response.status_code == 201

    result = response.json()
    assert result.get("id") == mock_order.id
    assert result.get("status") == mock_order.status.value
    assert result.get("created_on") == mock_order.created_on
    assert result.get("updated_on") == mock_order.updated_on
    assert result.get("user_id") == mock_order.user_id


def test_update_order(client, mock_order, mocker):
    mocker.patch('app.routes.order.OrderStatus.from_string', return_value=OrderStatus.PLACED)
    mocker.patch('app.routes.order.query_order', return_value=mock_order)

    mock_order.status = OrderStatus.PROCESSING
    mocker.patch('app.routes.order.update_order_db', return_value=mock_order)

    response = client.patch(
        url="/orders",
        json={
            "id": 1,
            "status": "PROCESSING",
        }
    )
    assert response.status_code == 200

    result = response.json()
    assert result.get("id") == mock_order.id
    assert result.get("status") == mock_order.status.value
    assert result.get("created_on") == mock_order.created_on
    assert result.get("updated_on") == mock_order.updated_on
    assert result.get("user_id") == mock_order.user_id


def test_update_order_with_non_existent_order_id(client, mocker):
    mocker.patch('app.routes.order.OrderStatus.from_string', return_value=OrderStatus.PLACED)
    mocker.patch('app.routes.order.query_order', return_value=None)

    response = client.patch(
        url="/orders",
        json={
            "id": 1,
            "status": "PROCESSING",
        }
    )
    assert response.status_code == 404

    result = response.json()
    assert result == {"detail": f"Order with id {1} does not exist."}


def test_update_order_with_invalid_order_status(client, mocker):
    mocker.patch('app.routes.order.OrderStatus.from_string', return_value=OrderStatus.UNKNOWN)

    response = client.patch(
        url="/orders",
        json={
            "id": 1,
            "status": "TEST",
        }
    )
    assert response.status_code == 404

    result = response.json()
    assert result == {"detail": f"Order Status is not valid, should be one of the following values {OrderStatus.list_values()}."}



