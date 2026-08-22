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

# The refresh token lives in an HttpOnly cookie — never in the JSON body.
# httpx's client jar stores it automatically after login, same as a browser.
REFRESH_COOKIE = "refresh_token"


def get_refresh_cookie(client) -> str | None:
    return client.cookies.get(REFRESH_COOKIE)


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
async def test_login_returns_access_token_and_sets_refresh_cookie(client):
    await client.post(REGISTER_URL, json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "SecurePass1"
    })
    response = await client.post(LOGIN_URL, json={
        "email": "login@example.com",
        "password": "SecurePass1"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    # Refresh token must NOT leak into the JS-readable body...
    assert "refresh_token" not in data
    # ...it arrives as an HttpOnly Set-Cookie instead.
    set_cookie = response.headers["set-cookie"]
    assert f"{REFRESH_COOKIE}=" in set_cookie
    assert "HttpOnly" in set_cookie
    assert get_refresh_cookie(client) is not None


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
async def test_refresh_rotates_cookie_pair(client):
    await register_and_login(client)
    old_refresh = get_refresh_cookie(client)
    assert old_refresh is not None
    response = await client.post(REFRESH_URL)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    new_refresh = get_refresh_cookie(client)
    assert new_refresh is not None
    assert new_refresh != old_refresh


@pytest.mark.asyncio
async def test_refresh_rotates_and_old_token_rejected(client):
    await register_and_login(client, email="rotate@example.com", username="rotateuser")
    old_refresh = get_refresh_cookie(client)
    response = await client.post(REFRESH_URL)
    assert response.status_code == 200
    client.cookies.clear()
    response = await client.post(REFRESH_URL, json={"refresh_token": old_refresh})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_invalid_token(client):
    response = await client.post(REFRESH_URL, json={"refresh_token": "not-a-valid-token"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_without_any_credentials(client):
    client.cookies.clear()
    response = await client.post(REFRESH_URL)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_with_access_token_rejected(client):
    login = await register_and_login(client, email="misuse@example.com", username="misuseuser")
    client.cookies.clear()
    response = await client.post(REFRESH_URL, json={"refresh_token": login.json()["access_token"]})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client):
    login = await register_and_login(client, email="logout@example.com", username="logoutuser")
    token = login.json()["access_token"]
    refresh_token = get_refresh_cookie(client)

    logout = await client.post(
        LOGOUT_URL,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout.status_code == 204

    # Cookie cleared client-side by the logout response itself...
    cleared = logout.headers.get("set-cookie", "")
    assert 'Max-Age=0' in cleared or 'expires=' in cleared

    # ...and revoked server-side: replaying the old value must fail.
    response = await client.post(REFRESH_URL, json={"refresh_token": refresh_token})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_persists_refresh_token(client):
    await register_and_login(client, email="persist@example.com", username="persist10")

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
    access = login1.json()["access_token"]
    refresh1 = get_refresh_cookie(client)
    login2 = await client.post(LOGIN_URL, json={"email": "multi@example.com", "password": "SecurePass1"})
    refresh2 = get_refresh_cookie(client)

    assert login1.status_code == 200 and login2.status_code == 200
    assert refresh1 != refresh2

    response = await client.post(LOGOUT_ALL_URL, headers={"Authorization": f"Bearer {access}"})
    assert response.status_code == 204

    assert (await client.post(REFRESH_URL, json={"refresh_token": refresh1})).status_code == 401
    assert (await client.post(REFRESH_URL, json={"refresh_token": refresh2})).status_code == 401


def refresh_token_from_set_cookie(response) -> str:
    """Pull the raw refresh token out of a response's Set-Cookie header."""
    header = response.headers["set-cookie"]
    value = header.split(f"{REFRESH_COOKIE}=", 1)[1]
    return value.split(";", 1)[0]


@pytest.mark.asyncio
async def test_logout_rejects_another_users_token(client):
    await client.post(REGISTER_URL, json={
        "email": "ownera@example.com", "username": "ownera", "password": "SecurePass1"
    })
    await client.post(REGISTER_URL, json={
        "email": "ownerb@example.com", "username": "ownerb", "password": "SecurePass1"
    })
    login_a = await client.post(LOGIN_URL, json={"email": "ownera@example.com", "password": "SecurePass1"})
    access_a = login_a.json()["access_token"]

    login_b = await client.post(LOGIN_URL, json={"email": "ownerb@example.com", "password": "SecurePass1"})
    refresh_b = refresh_token_from_set_cookie(login_b)

    response = await client.post(
        LOGOUT_URL,
        json={"refresh_token": refresh_b},
        headers={"Authorization": f"Bearer {access_a}"},
    )
    assert response.status_code == 401

    assert (await client.post(REFRESH_URL, json={"refresh_token": refresh_b})).status_code == 200


@pytest.mark.asyncio
async def test_logout_all_requires_authentication(client):
    response = await client.post(LOGOUT_ALL_URL)
    assert response.status_code == 401
