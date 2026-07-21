import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING, GEOSPHERE
from app.core.config import settings
from app.core.logging import logger

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_db(cls):
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
        try:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.DB_NAME]
            # Verify connection
            await cls.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            await cls.create_indexes()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")

    @classmethod
    async def create_indexes(cls):
        logger.info("Ensuring database indexes...")
        try:
            # Users Index
            await cls.db.users.create_index([("email", ASCENDING)], unique=True)
            
            # Crime Records Indexes
            await cls.db.crime_records.create_indexes([
                IndexModel([("district", ASCENDING)]),
                IndexModel([("police_station", ASCENDING)]),
                IndexModel([("crime_type", ASCENDING)]),
                IndexModel([("date", DESCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("location", GEOSPHERE)])
            ])

            # Chat History Indexes
            await cls.db.chat_history.create_index([("user_id", ASCENDING), ("timestamp", DESCENDING)])

            # Crime Predictions Indexes
            await cls.db.crime_predictions.create_index([("district", ASCENDING), ("date", DESCENDING)])

            # Crime Network Indexes
            await cls.db.crime_network.create_index([("criminal_id", ASCENDING)])

            # Alerts Indexes
            await cls.db.alerts.create_index([("district", ASCENDING), ("createdAt", DESCENDING)])

            logger.info("Database indexes successfully checked/created")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

# Dependency injection helpers
def get_db():
    if Database.db is None:
        raise Exception("Database not initialized")
    return Database.db

def get_collection(name: str):
    db = get_db()
    return db[name]
