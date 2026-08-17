import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from core.functions.jwt import create_access_token, create_refresh_token, decode_token
from domain.auth.usecauses.refresh_token_usecase import RefreshTokenUseCase

def test_jwt_token_payload():
    user_id = "user_123"
    role = "admin"

    # Access Token
    access_token = create_access_token(user_id=user_id, role=role)
    payload = decode_token(access_token)
    assert payload["id"] == user_id
    assert payload["role"] == role
    assert payload["type"] == "access"

    # Refresh Token
    refresh_token = create_refresh_token(user_id=user_id, role=role)
    refresh_payload = decode_token(refresh_token)
    assert refresh_payload["id"] == user_id
    assert refresh_payload["role"] == role
    assert refresh_payload["type"] == "refresh"

@pytest.mark.asyncio
async def test_refresh_token_usecase_success():
    refresh_token = create_refresh_token(user_id="u_999", role="user")
    use_case = RefreshTokenUseCase()

    res = await use_case.execute(refresh_token)
    assert res.is_success is True
    assert "access_token" in res.value
    assert "refresh_token" in res.value

    # Verify new tokens
    new_access_payload = decode_token(res.value["access_token"])
    assert new_access_payload["id"] == "u_999"
    assert new_access_payload["role"] == "user"

@pytest.mark.asyncio
async def test_refresh_token_usecase_invalid_type():
    # Pass access token instead of refresh token
    access_token = create_access_token(user_id="u_999", role="user")
    use_case = RefreshTokenUseCase()

    res = await use_case.execute(access_token)
    assert res.is_success is False
    assert "Invalid token type" in res.error

@pytest.mark.asyncio
async def test_refresh_endpoint_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register to get tokens
        reg_res = await client.post("/auth/register", json={
            "name": "JWT User",
            "age": 29,
            "email": "jwt_user@example.com",
            "password": "jwtpassword123"
        })
        assert reg_res.status_code == 201
        data = reg_res.json()
        assert "access_token" in data
        assert "refresh_token" in data

        refresh_token = data["refresh_token"]

        # Call /auth/refresh
        refresh_res = await client.post("/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert refresh_res.status_code == 200
        refreshed_data = refresh_res.json()
        assert "access_token" in refreshed_data
        assert "refresh_token" in refreshed_data
