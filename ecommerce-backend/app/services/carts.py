import uuid
from typing import cast

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
        cart = cast(Cart, cart)
        product_ids = list(updated_cart.items.keys())
        if not product_ids:
            return cart
        result = await session.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        products = result.scalars().all()
        products_map = {str(p.id): p for p in products}
        items = cart.items.copy()
        for p_id, quantity in updated_cart.items.items():
            product_id = str(p_id)
            product = products_map.get(product_id)
            CartService.validate_product_stock(product_id, product, quantity)
            items[product_id] = quantity
        cart.items = items
        await session.commit()
        return cart

    @staticmethod
    async def add_item_to_cart(
        session: AsyncSession,
        cart_id: int,
        product_id: str,
        quantity: int,
    ):
        cart = await CartService.get_cart(session, cart_id)
        cart = cast(Cart, cart)

        product = await session.get(Product, uuid.UUID(product_id))
        CartService.validate_product_stock(product_id, product, quantity)

        items = cart.items.copy()
        current_quantity = items.get(product_id, 0)
        new_quantity = current_quantity + quantity

        # Re-validate total quantity after addition
        CartService.validate_product_stock(product_id, product, new_quantity)

        items[product_id] = new_quantity
        cart.items = items
        await session.commit()
        return cart

    @staticmethod
    async def update_item_in_cart(
        session: AsyncSession,
        cart_id: int,
        product_id: str,
        quantity: int,
    ):
        cart = await CartService.get_cart(session, cart_id)
        cart = cast(Cart, cart)
        if product_id not in cart.items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not in cart",
            )
        product = await session.get(Product, uuid.UUID(product_id))
        CartService.validate_product_stock(product_id, product, quantity)

        items = cart.items.copy()
        items[product_id] = quantity
        cart.items = items
        await session.commit()
        return cart

    @staticmethod
    async def remove_item_from_cart(
        session: AsyncSession,
        cart_id: int,
        product_id: str,
    ):
        cart = await CartService.get_cart(session, cart_id)
        cart = cast(Cart, cart)
        if product_id not in cart.items:
            return cart
        items = cart.items.copy()
        del items[product_id]
        cart.items = items
        await session.commit()
        return cart

    @staticmethod
    def is_valid_cart(cart: Cart | None) -> bool:
        return bool(cart and cart.is_active)

    @staticmethod
    def is_cart_empty(cart: Cart):
        if not cart.items:
            return True
        for quantity in cart.items.values():
            if quantity > 0:
                return False
        return True

    @staticmethod
    def validate_product_stock(
        product_id: str, product: Product | None, quantity: int
    ) -> None:
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
