import pytest
from sqlalchemy import select
from app.models.refresh_token import RefreshToken
from tests.conftest import TestSessionLocal

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"
ME_URL = "/api/auth/me"
REFRESH_URL = "/api/auth/refresh"
LOGOUT_URL = "/api/auth/logout"
LOGOUT_ALL_URL = "/api/auth/logout-all"


async def register_and_login(client, email="refreshtest@example.com", username="refresh10"):
    await client.post(REGISTER_URL, json={
        "email": email, "username": username, "password": "SecurePass1"
    })
    return await client.post(LOGIN_URL, json={"email": email, "password": "SecurePass1"})


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


@pytest.mark.asyncio
async def test_refresh_returns_new_pair(client):
    login = await register_and_login(client)
    assert login.status_code == 200
    refresh_token = login.json()["refresh_token"]

    response = await client.post(REFRESH_URL, json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] != login.json()["access_token"]
    assert data["refresh_token"] != refresh_token


@pytest.mark.asyncio
async def test_refresh_rotates_and_old_token_rejected(client):
    login = await register_and_login(client, email="rotate@example.com", username="rotateuser")
    old_refresh = login.json()["refresh_token"]

    response = await client.post(REFRESH_URL, json={"refresh_token": old_refresh})
    assert response.status_code == 200

    # Old refresh token must now be rejected (rotation)
    response = await client.post(REFRESH_URL, json={"refresh_token": old_refresh})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_invalid_token(client):
    response = await client.post(REFRESH_URL, json={"refresh_token": "not-a-valid-token"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_with_access_token_rejected(client):
    login = await register_and_login(client, email="misuse@example.com", username="misuseuser")
    response = await client.post(REFRESH_URL, json={"refresh_token": login.json()["access_token"]})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client):
    login = await register_and_login(client, email="logout@example.com", username="logoutuser")
    token = login.json()["access_token"]
    refresh_token = login.json()["refresh_token"]

    logout = await client.post(
        LOGOUT_URL,
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout.status_code == 204

    # After logout the refresh token must be revoked
    response = await client.post(REFRESH_URL, json={"refresh_token": refresh_token})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_persists_refresh_token(client):
    login = await register_and_login(client, email="persist@example.com", username="persist10")
    assert login.status_code == 200

    async with TestSessionLocal() as db:
        result = await db.execute(select(RefreshToken))
        tokens = result.scalars().all()
    assert len(tokens) == 1
    assert tokens[0].revoked is False
    assert tokens[0].expires_at is not None


@pytest.mark.asyncio
async def test_logout_all_revokes_every_session(client):
    await client.post(REGISTER_URL, json={
        "email": "multi@example.com", "username": "multiuser", "password": "SecurePass1"
    })
    login1 = await client.post(LOGIN_URL, json={"email": "multi@example.com", "password": "SecurePass1"})
    login2 = await client.post(LOGIN_URL, json={"email": "multi@example.com", "password": "SecurePass1"})
    assert login1.status_code == 200 and login2.status_code == 200
    access = login1.json()["access_token"]
    refresh1 = login1.json()["refresh_token"]
    refresh2 = login2.json()["refresh_token"]

    response = await client.post(LOGOUT_ALL_URL, headers={"Authorization": f"Bearer {access}"})
    assert response.status_code == 204

    # Neither session remains usable after logout-all
    assert (await client.post(REFRESH_URL, json={"refresh_token": refresh1})).status_code == 401
    assert (await client.post(REFRESH_URL, json={"refresh_token": refresh2})).status_code == 401


@pytest.mark.asyncio
async def test_logout_rejects_another_users_token(client):
    await client.post(REGISTER_URL, json={
        "email": "ownera@example.com", "username": "ownera", "password": "SecurePass1"
    })
    await client.post(REGISTER_URL, json={
        "email": "ownerb@example.com", "username": "ownerb", "password": "SecurePass1"
    })
    login_a = await client.post(LOGIN_URL, json={"email": "ownera@example.com", "password": "SecurePass1"})
    login_b = await client.post(LOGIN_URL, json={"email": "ownerb@example.com", "password": "SecurePass1"})
    access_a = login_a.json()["access_token"]
    refresh_b = login_b.json()["refresh_token"]

    # A must not be able to revoke B's session
    response = await client.post(
        LOGOUT_URL,
        json={"refresh_token": refresh_b},
        headers={"Authorization": f"Bearer {access_a}"},
    )
    assert response.status_code == 401

    # B's refresh token is untouched and still usable
    assert (await client.post(REFRESH_URL, json={"refresh_token": refresh_b})).status_code == 200


@pytest.mark.asyncio
async def test_logout_all_requires_authentication(client):
    response = await client.post(LOGOUT_ALL_URL)
    assert response.status_code == 401