from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.order import insert_order
from app.crud.order import query_order
from app.crud.order import update_order as update_order_db
from app.data_access.database import get_db
from app.enums.order_status import OrderStatus
from app.schemas.order import OrderCreate
from app.schemas.order import OrderGet
from app.schemas.order import OrderUpdate

router = APIRouter()


@router.post("/orders", response_model=OrderGet, tags=["Orders"], status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    result = insert_order(db, order=order)

    return OrderGet(
        id=result.id,
        status=result.status.value,
        created_on=result.created_on,
        updated_on=result.updated_on,
        user_id=result.user_id,
    )


@router.patch("/orders", response_model=OrderGet, tags=["Orders"], status_code=200)
def update_order(order: OrderUpdate, db: Session = Depends(get_db)):
    if OrderStatus.from_string(order.status) == OrderStatus.UNKNOWN:
        raise HTTPException(
            status_code=404,
            detail=f"Order Status is not valid, should be one of the following values {OrderStatus.list_values()}."
        )
    if query_order(db, order_id=order.id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order.id} does not exist."
        )

    result = update_order_db(db, order=order)

    return OrderGet(
        id=result.id,
        status=result.status.value,
        created_on=result.created_on,
        updated_on=result.updated_on,
        user_id=result.user_id,
    )
