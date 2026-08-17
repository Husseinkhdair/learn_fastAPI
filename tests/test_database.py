import os
from unittest.mock import patch, MagicMock
import core.database as db_module

def test_database_configuration_reading():
    assert db_module.MONGODB_URL is not None
    assert "mongodb" in db_module.MONGODB_URL
    assert db_module.DB_NAME == "my_fastapi_db"

@patch("core.database.MongoClient")
def test_connect_and_get_database(mock_mongo_client):
    mock_client_instance = MagicMock()
    mock_mongo_client.return_value = mock_client_instance
    mock_db = MagicMock()
    mock_client_instance.__getitem__.return_value = mock_db

    # Reset manager state for test
    db_module.db_manager.client = None
    db_module.db_manager.db = None

    db = db_module.get_database()
    assert db == mock_db
    mock_mongo_client.assert_called_once_with(db_module.MONGODB_URL)

    # Cleanup state
    db_module.close_mongo_connection()
    assert db_module.db_manager.client is None
    assert db_module.db_manager.db is None
