from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.db import Order, OrderItem, Product, SessionDep, User
from app.schemas import OrderCreate, OrderRead
from app.services.orders import OrderService
from app.users import current_active_user, current_active_user_optional

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


@router.get("/orders/count")
async def count_orders(
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    query = select(func.count(Order.id)).where(Order.user_id == user.id)
    result = await session.execute(query)
    return {"count": result.scalar()}


@router.get("/orders/total-sales")
async def get_total_sales_price(
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    # Calculate total sales for all the orders
    query = (
        select(func.sum(Product.price * OrderItem.quantity))
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
    )
    result = await session.execute(query)
    total_sales = result.scalar() or 0
    return {"total_sales": total_sales}


@router.get("/orders/low-stock")
async def get_low_stock_items(
    session: SessionDep,
    user: User = Depends(current_active_user),
):
    query = select(Product).where(Product.stock < 30)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


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
