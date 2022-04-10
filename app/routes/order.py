from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.crud.order import insert_order
from app.crud.order import query_order
from app.crud.order import update_order as update_order_db
from app.database import get_db
from app.logic.order import validate_order_status
from app.schemas.order import OrderCreate
from app.schemas.order import OrderGet
from app.schemas.order import OrderUpdate

router = APIRouter()


@router.post("/api/v1/orders", response_model=OrderGet, tags=["Orders"], status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_db = insert_order(db, order=order)

    return OrderGet(
        id=order_db.id,
        status=order_db.status.value,
        created_on=order_db.created_on,
        updated_on=order_db.updated_on,
        user_id=order_db.user_id,
    )


@router.patch("/api/v1/orders", response_model=OrderGet, tags=["Orders"], status_code=status.HTTP_200_OK)
def update_order(order: OrderUpdate, db: Session = Depends(get_db)):
    validate_order_status(order_status=order.status)

    if query_order(db, order_id=order.id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
