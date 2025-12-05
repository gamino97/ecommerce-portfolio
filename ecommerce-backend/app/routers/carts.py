from fastapi import APIRouter, status

from app.db import SessionDep
from app.schemas import CartUpdate
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
)
async def update_cart(
    cart_id: int,
    updated_cart: CartUpdate,
    session: SessionDep,
):
    return await CartService.update_cart(
        session=session, cart_id=cart_id, updated_cart=updated_cart
    )
