import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import Cart, Product
from app.schemas import CartUpdate


class CartService:

    @staticmethod
    async def create_cart(
        session: AsyncSession,
        items: dict[str, int],
        user_id: uuid.UUID | None = None,
    ):
        cart = Cart(user_id=user_id, items=items)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
        return cart

    @staticmethod
    async def update_cart(
        session: AsyncSession,
        cart_id: int,
        updated_cart: CartUpdate,
    ):

        cart = await session.get(Cart, cart_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        for product_id, quantity in updated_cart.items.items():
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalars().one()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {product_id} not found",
                )
            if quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for product {product.name}",
                )
            cart.items[str(product_id)] = quantity
        await session.commit()
        return cart
