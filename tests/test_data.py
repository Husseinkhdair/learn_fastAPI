import pytest
from data.auth.data_sources.fack_auth_repository import FackAuthRepository
from domain.auth.entities.user_entitiy import UserDBEntity

@pytest.mark.asyncio
async def test_register_user_success():
    repo = FackAuthRepository()
    user_db = UserDBEntity(
        id="1",
        name="Ahmad",
        age=25,
        email="ahmad@example.com",
        password="secretpassword123",
        is_admin=False
    )
    result = await repo.register_user(user_db)
    assert result.is_success is True
    assert result.value.name == "Ahmad"
    assert result.value.id == "1"

@pytest.mark.asyncio
async def test_register_user_duplicate_error():
    repo = FackAuthRepository()
    user_db = UserDBEntity(
        id="1",
        name="Ahmad",
        age=25,
        email="ahmad@example.com",
        password="secretpassword123",
        is_admin=False
    )
    await repo.register_user(user_db)
    
    # Attempt second registration with same email
    duplicate_result = await repo.register_user(user_db)
    assert duplicate_result.is_success is False
    assert duplicate_result.error == "User already exists"

@pytest.mark.asyncio
async def test_login_user_success():
    repo = FackAuthRepository()
    user_db = UserDBEntity(
        id="1",
        name="Ahmad",
        age=25,
        email="ahmad@example.com",
        password="secretpassword123",
        is_admin=False
    )
    await repo.register_user(user_db)

    login_result = await repo.login_user("ahmad@example.com", "secretpassword123")
    assert login_result.is_success is True
    assert login_result.value.email == "ahmad@example.com" if hasattr(login_result.value, "email") else True

@pytest.mark.asyncio
async def test_login_user_not_found():
    repo = FackAuthRepository()
    login_result = await repo.login_user("nonexistent@example.com", "password123")
    assert login_result.is_success is False
    assert login_result.error == "User not found"

@pytest.mark.asyncio
async def test_login_user_invalid_password():
    repo = FackAuthRepository()
    user_db = UserDBEntity(
        id="1",
        name="Ahmad",
        age=25,
        email="ahmad@example.com",
        password="correct_password",
        is_admin=False
    )
    await repo.register_user(user_db)

    login_result = await repo.login_user("ahmad@example.com", "wrong_password")
    assert login_result.is_success is False
    assert login_result.error == "Invalid email or password"
