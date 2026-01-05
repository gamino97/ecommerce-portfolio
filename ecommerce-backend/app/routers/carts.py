import uuid

from fastapi import APIRouter, status

from app.db import SessionDep
from app.schemas import CartItemAdd, CartItemUpdate, CartRead, CartUpdate
from app.services.carts import CartService

router = APIRouter()


@router.post(
    "/carts",
    status_code=status.HTTP_201_CREATED,
)
async def create_cart(session: SessionDep):
    cart = await CartService.create_cart(session=session, items={})
    return str(cart.id)


@router.put(
    "/carts/{cart_id}",
    response_model=CartRead,
)
async def update_cart(
    cart_id: int,
    updated_cart: CartUpdate,
    session: SessionDep,
):
    return await CartService.update_cart(
        session=session, cart_id=cart_id, updated_cart=updated_cart
    )


@router.get("/carts/{cart_id}", response_model=CartRead)
async def get_cart(cart_id: int, session: SessionDep):
    return await CartService.get_cart(session=session, cart_id=cart_id)


@router.post("/carts/{cart_id}/items/", response_model=CartRead)
async def add_item_to_cart(
    cart_id: int,
    item: CartItemAdd,
    session: SessionDep,
):
    return await CartService.add_item_to_cart(
        session=session,
        cart_id=cart_id,
        product_id=str(item.product_id),
        quantity=item.quantity,
    )


@router.put("/carts/{cart_id}/items/{item_id}", response_model=CartRead)
async def update_item_in_cart(
    cart_id: int,
    item_id: uuid.UUID,
    item: CartItemUpdate,
    session: SessionDep,
):
    return await CartService.update_item_in_cart(
        session=session,
        cart_id=cart_id,
        product_id=str(item_id),
        quantity=item.quantity,
    )


@router.delete("/carts/{cart_id}/items/{item_id}", response_model=CartRead)
async def remove_item_from_cart(
    cart_id: int,
    item_id: uuid.UUID,
    session: SessionDep,
):
    return await CartService.remove_item_from_cart(
        session=session,
        cart_id=cart_id,
        product_id=str(item_id),
    )
