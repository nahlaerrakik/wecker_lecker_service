from fastapi import HTTPException
from fastapi import status

from app.enums.menu_type import MenuType
from app.enums.order_status import OrderStatus

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

INACTIVE_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user"
)


def raise_invalid_order_status_exception(order_status: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Invalid order_status {order_status}, should be one of the following values {OrderStatus.list_values()}.",
    )


def raise_invalid_menu_type_exception(menu_type: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Invalid menu_type {menu_type}, should be one of the following values {MenuType.list_values()}.",
    )


def raise_menu_id_not_found_exception(menu_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu with id {menu_id} does not exist.",
    )
