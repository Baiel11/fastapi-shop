import pytest

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"
ME_URL = "/api/auth/me"


@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post(REGISTER_URL, json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass1"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "username": "user1", "password": "SecurePass1"}
    await client.post(REGISTER_URL, json=payload)
    # second registration with the same email
    response = await client.post(REGISTER_URL, json={**payload, "username": "user2"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(REGISTER_URL, json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "SecurePass1"
    })
    response = await client.post(LOGIN_URL, json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "SecurePass1"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(REGISTER_URL, json={
        "email": "pw@example.com", "username": "pwuser", "password": "SecurePass1"
    })
    response = await client.post(LOGIN_URL, json={
        "email": "pw@example.com", "password": "WrongPass1"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authenticated(client):
    await client.post(REGISTER_URL, json={
        "email": "me@example.com", "username": "meuser", "password": "SecurePass1"
    })
    login = await client.post(LOGIN_URL, json={
        "email": "me@example.com", "password": "SecurePass1"
    })
    token = login.json()["access_token"]
    response = await client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    response = await client.get(ME_URL)
    assert response.status_code == 401