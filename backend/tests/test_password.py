import pytest

from tests.test_auth import (
    REGISTER_URL,
    LOGIN_URL,
    REFRESH_URL,
    REFRESH_COOKIE,
)

FORGOT_URL = "/api/auth/forgot-password"
RESET_URL = "/api/auth/reset-password"


def refresh_token_from_set_cookie(response) -> str:
    header = response.headers["set-cookie"]
    value = header.split(f"{REFRESH_COOKIE}=", 1)[1]
    return value.split(";", 1)[0]


@pytest.fixture
def captured_reset_emails(monkeypatch):
    """
    Replace the SMTP mailer with a recorder so tests can grab the raw reset
    link without sending real email or parsing logs. Patched at the import
    site (routes.customer.password), which is where the name is looked up.
    """
    sent: list[tuple[str, str]] = []

    async def fake_send_password_reset_email(to_email: str, reset_link: str) -> None:
        sent.append((to_email, reset_link))

    monkeypatch.setattr(
        "app.routes.customer.password.send_password_reset_email",
        fake_send_password_reset_email,
    )
    return sent


def token_from_link(link: str) -> str:
    return link.split("token=", 1)[1]


async def register_and_login(client, email, username):
    await client.post(REGISTER_URL, json={
        "email": email, "username": username, "password": "SecurePass1"
    })
    return await client.post(LOGIN_URL, json={"email": email, "password": "SecurePass1"})


@pytest.mark.asyncio
async def test_forgot_password_returns_204_for_existing_email(client, captured_reset_emails):
    await client.post(REGISTER_URL, json={
        "email": "forgot@example.com", "username": "forgotuser", "password": "SecurePass1"
    })
    response = await client.post(FORGOT_URL, json={"email": "forgot@example.com"})
    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.asyncio
async def test_forgot_password_is_identical_for_unknown_email(client, captured_reset_emails):
    """Enumeration defense: unknown emails get the same empty 204 and no
    email is generated."""
    known = await client.post(FORGOT_URL, json={"email": "forgot@example.com"})
    unknown = await client.post(FORGOT_URL, json={"email": "ghost@nowhere.com"})

    assert known.status_code == unknown.status_code == 204
    assert known.content == unknown.content == b""
    assert captured_reset_emails == []  # nothing sent for either address


@pytest.mark.asyncio
async def test_reset_password_with_valid_token(client, captured_reset_emails):
    await register_and_login(client, email="reset@example.com", username="resetuser")

    await client.post(FORGOT_URL, json={"email": "reset@example.com"})
    to_email, link = captured_reset_emails[0]
    assert to_email == "reset@example.com"

    response = await client.post(RESET_URL, json={
        "token": token_from_link(link),
        "password": "NewSecure2",
    })
    assert response.status_code == 204

    # New password accepted, old one rejected.
    old_login = await client.post(LOGIN_URL, json={
        "email": "reset@example.com", "password": "SecurePass1"
    })
    new_login = await client.post(LOGIN_URL, json={
        "email": "reset@example.com", "password": "NewSecure2"
    })
    assert old_login.status_code == 401
    assert new_login.status_code == 200


@pytest.mark.asyncio
async def test_reset_token_is_single_use(client, captured_reset_emails):
    await client.post(REGISTER_URL, json={
        "email": "single@example.com", "username": "singleuse", "password": "SecurePass1"
    })
    await client.post(FORGOT_URL, json={"email": "single@example.com"})
    _, link = captured_reset_emails[0]
    token = token_from_link(link)

    first = await client.post(RESET_URL, json={"token": token, "password": "NewSecure2"})
    replay = await client.post(RESET_URL, json={"token": token, "password": "Hacked123"})

    assert first.status_code == 204
    assert replay.status_code == 401

    hacked = await client.post(LOGIN_URL, json={
        "email": "single@example.com", "password": "Hacked123"
    })
    assert hacked.status_code == 401


@pytest.mark.asyncio
async def test_reset_rejects_invalid_and_expired_tokens(client):
    garbage = await client.post(RESET_URL, json={"token": "not-a-real-token", "password": "NewSecure2"})
    assert garbage.status_code == 401

    missing = await client.post(RESET_URL, json={"password": "NewSecure2"})
    assert missing.status_code == 422


@pytest.mark.asyncio
async def test_reset_rejects_weak_password(client, captured_reset_emails):
    await client.post(REGISTER_URL, json={
        "email": "weak@example.com", "username": "weakuser", "password": "SecurePass1"
    })
    await client.post(FORGOT_URL, json={"email": "weak@example.com"})
    _, link = captured_reset_emails[0]

    weak = await client.post(RESET_URL, json={"token": token_from_link(link), "password": "alllowercase1"})
    assert weak.status_code == 422

    # A rejected attempt must NOT burn the token — user can retry properly.
    retry = await client.post(RESET_URL, json={"token": token_from_link(link), "password": "NewSecure2"})
    assert retry.status_code == 204


@pytest.mark.asyncio
async def test_new_request_invalidates_previous_links(client, captured_reset_emails):
    """Requesting a second reset link must kill the first one."""
    await client.post(REGISTER_URL, json={
        "email": "twolink@example.com", "username": "twolinks", "password": "SecurePass1"
    })
    await client.post(FORGOT_URL, json={"email": "twolink@example.com"})
    _, first_link = captured_reset_emails[0]

    await client.post(FORGOT_URL, json={"email": "twolink@example.com"})
    _, second_link = captured_reset_emails[1]

    used_first = await client.post(RESET_URL, json={
        "token": token_from_link(first_link), "password": "NewSecure2"
    })
    used_second = await client.post(RESET_URL, json={
        "token": token_from_link(second_link), "password": "NewSecure2"
    })

    assert used_first.status_code == 401   # superseded
    assert used_second.status_code == 204  # newest link wins


@pytest.mark.asyncio
async def test_reset_revokes_all_existing_sessions(client, captured_reset_emails):
    """After a password reset, every previously issued session must be dead."""
    login = await register_and_login(client, email="kill@example.com", username="killsess")
    access_before = login.json()["access_token"]
    refresh_before = refresh_token_from_set_cookie(login)

    await client.post(FORGOT_URL, json={"email": "kill@example.com"})
    _, link = captured_reset_emails[0]

    reset = await client.post(RESET_URL, json={
        "token": token_from_link(link), "password": "NewSecure2",
    })
    assert reset.status_code == 204

    old_refresh = await client.post(REFRESH_URL, json={"refresh_token": refresh_before})
    assert old_refresh.status_code == 401

    me = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {access_before}"}
    )
    assert me.status_code == 200
