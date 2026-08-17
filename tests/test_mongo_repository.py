import pytest
from unittest.mock import MagicMock
from core.functions.security import hash_password
from data.auth.data_sources.mongo_auth_repository import MongoAuthRepository
from domain.auth.entities.user_entitiy import UserDBEntity

@pytest.mark.asyncio
async def test_mongo_auth_repository_register_success():
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = None  # No existing user

    repo = MongoAuthRepository(database=mock_db)
    user_db = UserDBEntity(
        id="gen_1",
        name="Mongo User",
        age=28,
        email="mongo_user@example.com",
        password="mongopassword123",
        is_admin=False
    )

    res = await repo.register_user(user_db)
    assert res.is_success is True
    assert res.value.name == "Mongo User"
    mock_collection.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_mongo_auth_repository_register_duplicate():
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {"email": "mongo_user@example.com"}  # User exists

    repo = MongoAuthRepository(database=mock_db)
    user_db = UserDBEntity(
        id="gen_1",
        name="Mongo User",
        age=28,
        email="mongo_user@example.com",
        password="mongopassword123",
        is_admin=False
    )

    res = await repo.register_user(user_db)
    assert res.is_success is False
    assert res.error == "User already exists"

@pytest.mark.asyncio
async def test_mongo_auth_repository_login_success():
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {
        "id": "gen_1",
        "name": "Mongo User",
        "age": 28,
        "email": "mongo_user@example.com",
        "password": hash_password("correctpassword"),
        "is_admin": False
    }

    repo = MongoAuthRepository(database=mock_db)
    res = await repo.login_user("mongo_user@example.com", "correctpassword")
    assert res.is_success is True
    assert res.value.name == "Mongo User"

@pytest.mark.asyncio
async def test_mongo_auth_repository_login_user_not_found():
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = None

    repo = MongoAuthRepository(database=mock_db)
    res = await repo.login_user("nonexistent@example.com", "password")
    assert res.is_success is False
    assert res.error == "User not found"
