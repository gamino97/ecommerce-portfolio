import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User


@pytest.fixture
async def user(session: AsyncSession):
    """Create a sample user for tests."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        first_name="Test",
        last_name="User",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_read_customers(auth_client: AsyncClient, user: User):
    response = await auth_client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Check if the created user is in the list
    assert any(u["email"] == user.email for u in data)
    assert any(u["first_name"] == user.first_name for u in data)


@pytest.mark.asyncio
async def test_read_customers_unauthorized(client: AsyncClient):
    response = await client.get("/customers/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.asyncio
async def test_read_customers_count(auth_client: AsyncClient, user: User):
    response = await auth_client.get("/customers/count")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["count"], int)
    assert data["count"] == 2


@pytest.mark.asyncio
async def test_read_customers_count_unauthorized(client: AsyncClient):
    response = await client.get("/customers/count")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
