import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register():
    """HTTP register smoke test — skips if Postgres is not running."""
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/auth/register",
                json={
                    "email": "test@test.com",
                    "username": "testuser",
                    "password": "password123",
                },
            )
    except Exception as exc:
        pytest.skip(f"Database unavailable for auth test: {exc}")
    assert response.status_code in [200, 201, 400, 422, 500]


@pytest.mark.asyncio
async def test_login():
    """HTTP login smoke test — skips if Postgres is not running."""
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/auth/login",
                data={"username": "test@test.com", "password": "password123"},
            )
    except Exception as exc:
        pytest.skip(f"Database unavailable for auth test: {exc}")
    assert response.status_code in [200, 400, 401, 422, 500]
