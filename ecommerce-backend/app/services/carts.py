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
    async def get_cart(session: AsyncSession, cart_id: int):
        cart = await session.get(Cart, cart_id)
        if not CartService.is_valid_cart(cart):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        return cart

    @staticmethod
    async def update_cart(
        session: AsyncSession,
        cart_id: int,
        updated_cart: CartUpdate,
    ):
        cart = await session.get(Cart, cart_id)
        if not CartService.is_valid_cart(cart):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        product_ids = list(updated_cart.items.keys())
        if not product_ids:
            return cart
        result = await session.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        products = result.scalars().all()
        products_map = {p.id: p for p in products}
        for product_id, quantity in updated_cart.items.items():
            product = products_map.get(product_id)
            CartService.validate_product_stock(product_id, product, quantity)
            cart.items[str(product_id)] = quantity
        await session.commit()
        return cart

    @staticmethod
    def is_valid_cart(cart: Cart):
        return cart and cart.is_active

    @staticmethod
    def is_cart_empty(cart: Cart):
        return not cart.items

    @staticmethod
    def validate_product_stock(
        product_id: int, product: Product, quantity: int
    ):
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found in cart",
            )
        if quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product {product.name}",
            )
