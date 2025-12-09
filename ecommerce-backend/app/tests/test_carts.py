import uuid

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Cart, Product, User
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_cart(session: AsyncSession, super_user: User):
    product_id = str(uuid.uuid4())
    user = super_user
    cart = Cart(user_id=user.id, items={product_id: 1})
    session.add(cart)
    await session.commit()
    assert cart.id is not None
    assert cart.user == user
    assert cart.items == {product_id: 1}


@pytest.mark.asyncio
async def test_create_cart_router(client: AsyncClient):
    response = await client.post("/carts")
    assert response.status_code == 201
    assert type(response.json()) == str


@pytest.mark.asyncio
async def test_update_cart_router(
    client: AsyncClient, cart: Cart, product: Product
):
    response = await client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 1}}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["items"] == {str(product.id): 1}
    assert cart.items == {str(product.id): 1}


@pytest.mark.asyncio
async def test_update_cart_router_invalid_cart(
    client: AsyncClient, cart: Cart, session: AsyncSession
):
    response = await client.put("/carts/0", json={"items": {}})
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart not found"}
    cart.is_active = False
    session.add(cart)
    await session.commit()
    response = await client.put(f"/carts/{cart.id}", json={"items": {}})
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart not found"}


@pytest.mark.asyncio
async def test_update_cart_product_invalid_stock(
    client: AsyncClient, cart: Cart, product: Product
):
    response = await client.put(
        f"/carts/{cart.id}",
        json={"items": {str(product.id): product.stock + 1}},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Not enough stock for product {product.name}"
    }


@pytest.mark.asyncio
async def test_get_cart(
    client: AsyncClient, cart: Cart, product: Product, session: AsyncSession
):
    cart.items = {str(product.id): 1}
    session.add(cart)
    await session.commit()
    response = await client.get(f"/carts/{cart.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == {str(product.id): 1}
    assert data["user_id"] == cart.user_id
    assert data["id"] == cart.id


@pytest.mark.asyncio
async def test_update_cart_product_invalid_quantity(
    client: AsyncClient, cart: Cart, product: Product
):
    response = await client.put(
        f"/carts/{cart.id}",
        json={"items": {str(product.id): -1}},
    )
    assert response.status_code == 422
