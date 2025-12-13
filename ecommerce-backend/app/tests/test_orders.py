import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import Cart, Order, OrderItem, Product, User
from app.schemas import OrderRead, OrderReadWithUser


@pytest.mark.asyncio
async def test_create_order(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
    session: AsyncSession,
    super_user: User,
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 12}}
    )
    initial_product_stock = product.stock
    assert response.status_code == 200
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": "123 Main St, Anytown, USA"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["shipping_address"] == "123 Main St, Anytown, USA"
    assert data["order_items"][0]["product_id"] == str(product.id)
    assert data["order_items"][0]["quantity"] == 12
    assert data["created_at"] is not None
    assert data["status"] == "pending"
    assert data["total_price"] == str(product.price * 12)
    await session.refresh(product)
    assert product.stock == initial_product_stock - 12


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


@pytest.mark.asyncio
async def test_create_order_invalid_quantity(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): -1}}
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be greater than or equal to 0"
    )


@pytest.mark.asyncio
async def test_create_order_too_many_items(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
):
    response = await auth_client.put(
        f"/carts/{cart.id}",
        json={"items": {str(product.id): product.stock + 2}},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == f"Not enough stock for product {product.name}"
    )


@pytest.mark.asyncio
async def test_count_orders_superuser(auth_client: AsyncClient):
    response = await auth_client.get("/orders/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_count_orders_unauthorized(client: AsyncClient):
    response = await client.get("/orders/count")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.asyncio
async def test_get_total_sales_price_superuser(
    auth_client: AsyncClient,
    product: Product,
    session: AsyncSession,
    super_user: User,
):
    response = await auth_client.get("/orders/total-sales")
    assert response.status_code == 200
    assert response.json() == {"total_sales": "0"}
    order = Order(
        user=super_user,
        shipping_address="123 Main St, Anytown, USA",
        status="pending",
    )
    session.add(order)
    await session.flush()
    order_item = OrderItem(
        order=order,
        product=product,
        quantity=2,
        price=product.price,
    )
    session.add(order_item)
    await session.commit()
    response = await auth_client.get("/orders/total-sales")
    assert response.status_code == 200
    assert str(response.json().get("total_sales")) == str(product.price * 2)


@pytest.mark.asyncio
async def test_get_total_sales_price_unauthorized(client: AsyncClient):
    response = await client.get("/orders/total-sales")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.asyncio
async def test_get_all_orders_superuser(auth_client: AsyncClient):
    response = await auth_client.get("/orders/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_all_orders_unauthorized(client: AsyncClient):
    response = await client.get("/orders/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.asyncio
async def test_get_all_orders_order_schema_validation(
    auth_client: AsyncClient,
    product: Product,
    cart: Cart,
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 5}}
    )
    assert response.status_code == 200
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": "456 Schema Ln, Validate City, VC"},
    )
    assert response.status_code == 201
    response = await auth_client.get("/orders/")
    assert response.status_code == 200
    data_list = response.json()
    assert len(data_list) == 1
    data = data_list[0]
    order = OrderReadWithUser.model_validate(data)
    assert order.shipping_address == "456 Schema Ln, Validate City, VC"
    assert len(order.order_items) == 1
    assert order.order_items[0].product_id == product.id
    assert order.total_price == product.price * 5


@pytest.mark.asyncio
async def test_get_order(
    auth_client: AsyncClient, product: Product, cart: Cart
):
    response = await auth_client.put(
        f"/carts/{cart.id}", json={"items": {str(product.id): 5}}
    )
    assert response.status_code == 200
    response = await auth_client.post(
        f"/carts/{cart.id}/orders/",
        json={"shipping_address": "456 Schema Ln, Validate City, VC"},
    )
    assert response.status_code == 201
    order_id = response.json()["id"]
    response = await auth_client.get(f"/orders/{order_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_order_unauthorized(client: AsyncClient):
    response = await client.get("/orders/1")
    assert response.status_code == 401
