import pytest

CATEGORIES_URL = "/api/categories"


@pytest.mark.asyncio
async def test_get_categories_empty(client):
    response = await client.get(CATEGORIES_URL)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_category_not_found(client):
    response = await client.get(f"{CATEGORIES_URL}/999")
    assert response.status_code == 404
