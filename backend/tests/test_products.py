import pytest

PRODUCTS_URL = "/api/products"


@pytest.mark.asyncio
async def test_get_products_empty(client):
    response = await client.get(PRODUCTS_URL)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_product_not_found(client):
    response = await client.get(f"{PRODUCTS_URL}/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_products_by_category_not_found(client):
    response = await client.get(f"{PRODUCTS_URL}/category/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_pagination_defaults(client):
    response = await client.get(PRODUCTS_URL)
    assert response.status_code == 200
    data = response.json()
    assert "page" in data
    assert "size" in data
    assert "pages" in data
    assert data["page"] == 1
