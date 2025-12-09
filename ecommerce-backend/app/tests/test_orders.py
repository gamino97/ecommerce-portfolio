import pytest
from faker import Faker
from httpx import AsyncClient

from app.db import Cart, Product, User


@pytest.mark.asyncio
async def test_create_order(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
    super_user: User,
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 1}}
    )
    assert response.status_code == 200
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": "123 Main St, Anytown, USA"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["user_id"] == str(super_user.id)
    assert data["shipping_address"] == "123 Main St, Anytown, USA"
    assert data["order_items"][0]["product_id"] == str(product.id)
    assert data["order_items"][0]["quantity"] == 1
    assert data["created_at"] is not None
    assert data["status"] == "pending"
    assert data["total_price"] == str(product.price)


@pytest.mark.asyncio
async def test_create_order_invalid_cart_id(auth_client: AsyncClient):
    response = await auth_client.post(
        "/carts/0/orders/",
        json={"shipping_address": "123 Main St, Anytown, USA"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart is not active"}


@pytest.mark.asyncio
async def test_create_order_cart_empty(
    auth_client: AsyncClient,
    cart: Cart,
    product: Product,
):
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": "123 Main St, Anytown, USA"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cart is empty"}
    cart.items = {str(product.id): 0}
    await auth_client.put(f"/carts/{cart.id}", json={"items": cart.items})

    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": "123 Main St, Anytown, USA"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cart is empty"}


@pytest.mark.asyncio
async def test_create_order_empty_shipping_address(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 1}}
    )
    assert response.status_code == 200
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": ""},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "String should have at least 1 character"
    )


@pytest.mark.asyncio
async def test_create_order_too_long_shipping_address(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
    faker: Faker,
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 1}}
    )
    assert response.status_code == 200
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": faker.pystr(min_chars=201, max_chars=201)},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "String should have at most 200 characters"
    )
