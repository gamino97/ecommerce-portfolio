import pytest
from httpx import AsyncClient

from app.db import Category


@pytest.mark.asyncio
async def test_get_all_categories(client: AsyncClient, category: Category):
    response = await client.get("/categories/")
    assert response.status_code == 200
    data = response.json()[0]
    assert data["name"] == category.name
    assert data["id"] == str(category.id)
