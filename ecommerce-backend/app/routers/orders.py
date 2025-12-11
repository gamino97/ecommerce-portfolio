import decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import Order, SessionDep, User
from app.schemas import OrderCreate, OrderRead, OrderReadWithUser
from app.services.orders import OrderService
from app.users import current_active_user, current_superuser

router = APIRouter()


@router.get("/orders/user", response_model=list[OrderRead])
async def get_user_orders(
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    query = (
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.user_id == user.id)
    )
    result = await session.execute(query)
    return result.scalars().all()


@router.get(
    "/orders/",
    response_model=list[OrderReadWithUser],
    dependencies=[Depends(current_superuser)],
)
async def read_orders(
    session: SessionDep,
):
    query = select(Order).options(
        selectinload(Order.order_items), selectinload(Order.user)
    )
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/orders/count", dependencies=[Depends(current_superuser)])
async def count_orders(session: SessionDep) -> dict[str, int]:
    return await OrderService.get_all_orders_count(session)


@router.get("/orders/total-sales", dependencies=[Depends(current_superuser)])
async def get_total_sales_price(
    session: SessionDep,
) -> dict[str, decimal.Decimal]:
    return await OrderService.get_total_sales_price(session)


@router.get("/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    query = (
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == order_id, Order.user_id == user.id)
    )
    result = await session.execute(query)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


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
