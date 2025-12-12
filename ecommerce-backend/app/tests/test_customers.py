import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User


@pytest.mark.asyncio
async def test_read_customers(auth_client: AsyncClient, user: User):
    import datetime

    response = await auth_client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Check if the created user is in the list
    assert any(u["email"] == user.email for u in data)
    assert any(u["first_name"] == user.first_name for u in data)
    assert any(u["last_name"] == user.last_name for u in data)
    assert any(
        datetime.datetime.fromisoformat(u["created_at"]) == user.created_at
        for u in data
    )


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
