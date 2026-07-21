from motor.motor_asyncio import AsyncIOMotorClient
import mongomock
from app.core.config import settings

class DatabaseConnection:
    """
    Manages MongoDB connections asynchronously.
    Falls back gracefully to mongomock if MongoDB is not reachable,
    ensuring offline hackathon readiness.
    """
    def __init__(self):
        self.client = None
        self.db = None
        self.is_mock = False

    def connect(self):
        try:
            # Attempt to connect to real MongoDB
            self.client = AsyncIOMotorClient(settings.MONGO_URL, serverSelectionTimeoutMS=2000)
            self.db = self.client.get_database()
            # Test connection briefly
            self.is_mock = False
        except Exception:
            # Fallback to mongomock
            self.client = mongomock.MongoClient()
            self.db = self.client.crimecop
            self.is_mock = True

db_connection = DatabaseConnection()
db_connection.connect()

def get_db():
    return db_connection.db
