import uuid
from typing import Callable, Coroutine

import pytest
from httpx import AsyncClient

from app.db import Category, Product


@pytest.mark.asyncio
async def test_read_products(client: AsyncClient):
    response = await client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_unauthorized_product(client: AsyncClient):
    response = await client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A test product",
            "image_url": "http://example.com/image.png",
            "price": 10.99,
            "stock": 100,
            "category_id": "invalid_id",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_product_authorized(
    auth_client: AsyncClient, category: Category
):
    response = await auth_client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A test product",
            "image_url": "http://example.com/image.png",
            "price": 10.99,
            "stock": 100,
            "category_id": str(category.id),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["category_id"] == str(category.id)
    assert "id" in data


@pytest.mark.asyncio
async def test_create_product_invalid_category(auth_client: AsyncClient):
    response = await auth_client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A test product",
            "image_url": "http://example.com/image.png",
            "price": 10.99,
            "stock": 100,
            "category_id": "invalid_id",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_product_nonexistent_category(auth_client: AsyncClient):
    random_id = uuid.uuid4()
    response = await auth_client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A test product",
            "image_url": "http://example.com/image.png",
            "price": 10.99,
            "stock": 100,
            "category_id": str(random_id),
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid category_id"


@pytest.mark.asyncio
async def test_create_product_required_fields(auth_client: AsyncClient):
    product_information = {
        "name": "Test Product",
        "description": "A test product",
        "image_url": "http://example.com/image.png",
        "price": 10.99,
        "stock": 100,
        "category_id": "invalid_id",
    }
    product_information_without_name = product_information.copy()
    product_information_without_name.pop("name")
    response = await auth_client.post(
        "/products/",
        json=product_information_without_name,
    )
    # Continue with all the other fields
    product_information_without_description = product_information.copy()
    product_information_without_description.pop("description")
    response = await auth_client.post(
        "/products/",
        json=product_information_without_description,
    )
    assert response.status_code == 422
    product_information_without_image_url = product_information.copy()
    product_information_without_image_url.pop("image_url")
    response = await auth_client.post(
        "/products/",
        json=product_information_without_image_url,
    )
    assert response.status_code == 422
    product_information_without_price = product_information.copy()
    product_information_without_price.pop("price")
    response = await auth_client.post(
        "/products/",
        json=product_information_without_price,
    )
    assert response.status_code == 422
    product_information_without_stock = product_information.copy()
    product_information_without_stock.pop("stock")
    response = await auth_client.post(
        "/products/",
        json=product_information_without_stock,
    )
    assert response.status_code == 422
    product_information_without_category_id = product_information.copy()
    product_information_without_category_id.pop("category_id")
    response = await auth_client.post(
        "/products/",
        json=product_information_without_category_id,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_product_price_negative(
    auth_client: AsyncClient, category: Category
):
    product_information = {
        "name": "Test Product",
        "description": "A test product",
        "image_url": "http://example.com/image.png",
        "price": -10.99,
        "stock": 100,
        "category_id": str(category.id),
    }
    response = await auth_client.post(
        "/products/",
        json=product_information,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_product(
    auth_client: AsyncClient, client: AsyncClient, category: Category
):
    # Create a product first
    create_response = await auth_client.post(
        "/products/",
        json={
            "name": "Product to Read",
            "description": "Read me",
            "image_url": "http://example.com/read.png",
            "price": 5.00,
            "stock": 10,
            "category_id": str(category.id),
        },
    )
    print(create_response.json())
    product_id = create_response.json()["id"]

    response = await client.get(f"/products/{product_id}")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Product to Read"


@pytest.mark.asyncio
async def test_update_product_unauthorized(
    client: AsyncClient, product: Product
):
    response = await client.patch(
        f"/products/{product.id}",
        json={"price": 25.00, "name": "Updated Product"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_product(
    auth_client: AsyncClient,
    product: Product,
):
    product_id = product.id
    response = await auth_client.patch(
        f"/products/{product_id}",
        json={"price": 25.00, "name": "Updated Product"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == "25.00"
    assert data["name"] == "Updated Product"
    # Check if other fields remain
    assert data["description"] == "A test product"


@pytest.mark.asyncio
async def test_update_product_category(
    auth_client: AsyncClient,
    product: Product,
    create_category: Callable[[str], Coroutine[None, None, Category]],
):
    product_id = product.id
    new_category = await create_category("New Category")
    assert product.category_id != new_category.id

    response = await auth_client.patch(
        f"/products/{product_id}",
        json={"category_id": str(new_category.id)},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == str(new_category.id)


@pytest.mark.asyncio
async def test_update_product_invalid_category(
    auth_client: AsyncClient,
    product: Product,
):
    random_id = uuid.uuid4()
    product_id = product.id
    response = await auth_client.patch(
        f"/products/{product_id}",
        json={"category_id": str(random_id)},
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid category_id"


@pytest.mark.asyncio
async def test_read_nonexistent_product(client: AsyncClient):
    random_id = uuid.uuid4()
    response = await client.get(f"/products/{random_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_nonexistent_product(auth_client: AsyncClient):
    random_id = uuid.uuid4()
    response = await auth_client.patch(
        f"/products/{random_id}", json={"price": 100.00}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_low_stock_products_count(auth_client: AsyncClient):
    response = await auth_client.get("/products/low-stock/count")
    assert response.status_code == 200
    assert response.json()["count"] == 0


@pytest.mark.asyncio
async def test_get_low_stock_products_count_many(
    auth_client: AsyncClient,
    create_product,
    category: Category,
):
    await create_product("Product 1", stock=20, category=category)
    await create_product("Product 2", category=category)
    await create_product("Product 3", category=category)
    response = await auth_client.get("/products/low-stock/count")
    assert response.status_code == 200
    assert response.json()["count"] == 1


@pytest.mark.asyncio
async def test_get_low_stock_products_count_unauthorized(client: AsyncClient):
    response = await client.get("/products/low-stock/count")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
