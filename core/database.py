import os
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

# Load environment variables from .env file
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URI") or os.getenv("MONGODB_URL", "mongodb+srv://hussein:<db_password>@cluster0.ytfjnm0.mongodb.net/?appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "my_fastapi_db")

class MongoDB:
    client: Optional[MongoClient] = None
    db: Optional[Database] = None

db_manager = MongoDB()

def connect_to_mongo():
    """Initializes MongoDB connection singleton."""
    if db_manager.client is None:
        db_manager.client = MongoClient(MONGODB_URL)
        db_manager.db = db_manager.client[DB_NAME]
    return db_manager.db

def close_mongo_connection():
    """Closes MongoDB connection."""
    if db_manager.client:
        db_manager.client.close()
        db_manager.client = None
        db_manager.db = None

def get_database() -> Database:
    """Dependency / helper function to obtain PyMongo Database instance."""
    if db_manager.db is None:
        connect_to_mongo()
    return db_manager.db

def get_mongo_client() -> MongoClient:
    """Returns PyMongo client instance."""
    if db_manager.client is None:
        connect_to_mongo()
    return db_manager.client

def ping_database() -> bool:
    """Pings MongoDB to verify connection status."""
    try:
        client = get_mongo_client()
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB connection ping failed: {e}")
        return False
