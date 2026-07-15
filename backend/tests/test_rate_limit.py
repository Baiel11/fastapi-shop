import pytest
from app.core.limiter import limiter

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"


@pytest.mark.asyncio
async def test_login_rate_limit(client):
    """
    Sends 6 login attempts (limit is 5/minute) and expects a 429 on the last one.
    """
    limiter.enabled = True

    for i in range(5):
        await client.post(LOGIN_URL, json={
            "email": f"user{i}@test.com",
            "password": "wrongpassword"
        })

    # 6th request should be rate-limited
    response = await client.post(LOGIN_URL, json={
        "email": "user6@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 429
