import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_register_endpoint_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "name": "Test User",
            "age": 25,
            "email": "unique_api_user@example.com",
            "password": "validpassword123"
        })
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert "access_token" in data
    assert "user" in data

@pytest.mark.asyncio
async def test_register_endpoint_duplicate_email_400():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "name": "Test User",
            "age": 25,
            "email": "duplicate_api@example.com",
            "password": "validpassword123"
        }
        # First registration
        r1 = await client.post("/auth/register", json=payload)
        assert r1.status_code == 201

        # Second registration with same email
        r2 = await client.post("/auth/register", json=payload)
        assert r2.status_code == 400
        assert r2.json()["detail"] == "User already exists"

@pytest.mark.asyncio
async def test_register_endpoint_validation_error_422():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Invalid payload (short password)
        response = await client.post("/auth/register", json={
            "name": "Test User",
            "age": 25,
            "email": "user@example.com",
            "password": "123"  # too short
        })
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_endpoint_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register user first
        await client.post("/auth/register", json={
            "name": "Login User",
            "age": 30,
            "email": "login_user@example.com",
            "password": "loginpassword123"
        })

        # Perform login
        response = await client.post("/auth/login", json={
            "email": "login_user@example.com",
            "password": "loginpassword123"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

@pytest.mark.asyncio
async def test_login_endpoint_failed_400():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/login", json={
            "email": "unknown@example.com",
            "password": "wrongpassword123"
        })
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"
