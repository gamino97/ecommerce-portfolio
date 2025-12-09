from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.strategy_options import selectinload

from app.db import Cart, Order, OrderItem, Product, User
from app.schemas import OrderCreate
from app.services.carts import CartService


class OrderService:
    @staticmethod
    async def create_order(
        session: AsyncSession,
        order_create: OrderCreate,
        cart_id: int,
        user: User,
    ):
        result = await session.execute(select(Cart).where(Cart.id == cart_id))
        cart = result.scalar_one_or_none()
        if not CartService.is_valid_cart(cart):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart is not active",
            )
        if CartService.is_cart_empty(cart):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty",
            )
        product_ids = list(cart.items.keys())
        result = await session.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        products = result.scalars().all()
        products_map = {str(p.id): p for p in products}
        order = Order(
            status="pending",
            shipping_address=order_create.shipping_address,
            user=user,
        )
        session.add(order)
        await session.flush()  # To get order.id
        for product_id, quantity in cart.items.items():
            product = products_map.get(product_id)
            CartService.validate_product_stock(product_id, product, quantity)
            product.stock -= quantity
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
            )
            session.add(order_item)
        cart.is_active = False
        await session.commit()
        # Refresh to load relationships
        query = (
            select(Order)
            .options(
                selectinload(Order.order_items).selectinload(OrderItem.product)
            )
            .where(Order.id == order.id)
        )
        result = await session.execute(query)
        created_order = result.scalar_one()
        return created_order
