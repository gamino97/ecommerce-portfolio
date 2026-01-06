import decimal
import uuid
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import Cart, Product
from app.schemas import (
    CartItemEnriched,
    CartRead,
    CartSummary,
    CartUpdate,
)


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
        return await CartService._get_cart_read_from_model(session, cart)

    @staticmethod
    async def get_cart(session: AsyncSession, cart_id: int):
        cart = await session.get(Cart, cart_id)
        if not CartService.is_valid_cart(cart):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        return await CartService._get_cart_read_from_model(
            session, cast(Cart, cart)
        )

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
            return await CartService._get_cart_read_from_model(session, cart)
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
        return await CartService._get_cart_read_from_model(session, cart)

    @staticmethod
    async def add_item_to_cart(
        session: AsyncSession,
        cart_id: int,
        product_id: str,
        quantity: int,
    ):
        cart_obj = await session.get(Cart, cart_id)
        if not CartService.is_valid_cart(cart_obj):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        cart = cast(Cart, cart_obj)

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
        return await CartService._get_cart_read_from_model(session, cart)

    @staticmethod
    async def update_item_in_cart(
        session: AsyncSession,
        cart_id: int,
        product_id: str,
        quantity: int,
    ):
        cart_obj = await session.get(Cart, cart_id)
        if not CartService.is_valid_cart(cart_obj):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        cart = cast(Cart, cart_obj)
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
        return await CartService._get_cart_read_from_model(session, cart)

    @staticmethod
    async def remove_item_from_cart(
        session: AsyncSession,
        cart_id: int,
        product_id: str,
    ):
        cart_obj = await session.get(Cart, cart_id)
        if not CartService.is_valid_cart(cart_obj):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
            )
        cart = cast(Cart, cart_obj)
        if product_id not in cart.items:
            return await CartService._get_cart_read_from_model(session, cart)
        items = cart.items.copy()
        del items[product_id]
        cart.items = items
        await session.commit()
        return await CartService._get_cart_read_from_model(session, cart)

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
    async def _get_cart_read_from_model(
        session: AsyncSession, cart: Cart
    ) -> CartRead:
        product_ids = [uuid.UUID(pid) for pid in cart.items.keys()]
        products_map = {}
        if product_ids:
            result = await session.execute(
                select(Product).where(Product.id.in_(product_ids))
            )
            products = result.scalars().all()
            products_map = {str(p.id): p for p in products}

        enriched_items = []
        subtotal = decimal.Decimal(0)
        total_items_count = 0

        for pid_str, quantity in cart.items.items():
            product = products_map.get(pid_str)
            if not product:
                continue

            unit_price = decimal.Decimal(str(product.price))
            line_total: decimal.Decimal = unit_price * quantity
            subtotal += line_total
            total_items_count += quantity

            enriched_items.append(
                CartItemEnriched(
                    product_id=uuid.UUID(pid_str),
                    name=product.name,
                    description=product.description,
                    image_url=product.image_url,
                    quantity=quantity,
                    price=product.price,
                    stock=product.stock,
                    line_total=line_total,
                )
            )

        grand_total = subtotal
        summary = CartSummary(
            subtotal=subtotal,
            grand_total=grand_total,
            total_items_count=total_items_count,
        )
        return CartRead(
            id=cart.id,
            user_id=cart.user_id,
            items=enriched_items,
            summary=summary,
            updated_at=cart.created_at,
        )

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
