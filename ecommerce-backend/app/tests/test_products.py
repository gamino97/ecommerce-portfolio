import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Category, Product


@pytest.fixture
async def category(session: AsyncSession):
    """Create a sample category for tests."""
    category = Category(name="Test Category")
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@pytest.fixture
async def product(session: AsyncSession, category: Category):
    """Create a sample product for tests."""
    product = Product(
        name="Test Product",
        description="A test product",
        image_url="http://example.com/image.png",
        price=10.99,
        stock=100,
        category_id=category.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


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
    auth_client: AsyncClient, client: AsyncClient, category: Category
):
    # Create a product first
    create_response = await auth_client.post(
        "/products/",
        json={
            "name": "Product to Update",
            "description": "Update me",
            "image_url": "http://example.com/update.png",
            "price": 20.00,
            "stock": 5,
            "category_id": str(category.id),
        },
    )
    product_id = create_response.json()["id"]

    response = await client.patch(
        f"/products/{product_id}",
        json={"price": 25.00, "name": "Updated Product"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 25.00
    assert data["name"] == "Updated Product"
    # Check if other fields remain
    assert data["description"] == "Update me"


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
