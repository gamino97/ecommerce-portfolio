import decimal

from fastapi import APIRouter, Depends, status

from app.db import SessionDep, User
from app.schemas import OrderCreate, OrderRead, OrderReadWithUser
from app.services.orders import OrderService
from app.users import current_active_user, current_superuser

router = APIRouter()


@router.get("/orders/user", response_model=list[OrderRead])
async def get_user_orders(
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    return await OrderService.get_user_orders(session, user)


@router.get(
    "/orders/",
    response_model=list[OrderReadWithUser],
    dependencies=[Depends(current_superuser)],
)
async def read_orders(
    session: SessionDep,
):
    return await OrderService.get_all_orders(session)


@router.get("/orders/count", dependencies=[Depends(current_superuser)])
async def count_orders(session: SessionDep) -> dict[str, int]:
    return await OrderService.get_all_orders_count(session)


@router.get("/orders/total-sales", dependencies=[Depends(current_superuser)])
async def get_total_sales_price(
    session: SessionDep,
) -> dict[str, decimal.Decimal]:
    return await OrderService.get_total_sales_price(session)


@router.get("/orders/{order_id}", response_model=OrderReadWithUser)
async def get_order(
    order_id: int,
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    return await OrderService.get_order(session, order_id, user)


@router.post(
    "/carts/{cart_id}/orders/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    cart_id: int,
    order_create: OrderCreate,
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    return await OrderService.create_order(session, order_create, cart_id, user)
