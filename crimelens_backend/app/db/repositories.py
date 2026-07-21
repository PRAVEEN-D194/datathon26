from datetime import datetime
from app.db.connection import get_db

class BaseRepository:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    def _get_collection(self):
        db = get_db()
        # In mongomock, it's synchronous; in Motor, it's standard property retrieval
        return db[self.collection_name]

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users")

    async def get_user_by_username(self, username: str) -> dict:
        col = self._get_collection()
        # Handle async call for motor or direct query for mongomock
        res = col.find_one({"username": username})
        if hasattr(res, "__await__"):
            res = await res
        return res

    async def create_user(self, user_data: dict) -> dict:
        col = self._get_collection()
        res = col.insert_one(user_data)
        if hasattr(res, "__await__"):
            await res
        return user_data

class CrimeRepository(BaseRepository):
    def __init__(self):
        super().__init__("crimes")

    async def get_all_crimes(self, skip: int = 0, limit: int = 10, district: str = None, crime_type: str = None) -> list:
        col = self._get_collection()
        query = {}
        if district:
            query["district"] = district
        if crime_type:
            query["crime_head"] = crime_type

        # Handle async cursor
        cursor = col.find(query).skip(skip).limit(limit)
        if hasattr(cursor, "to_list"):
            return await cursor.to_list(length=limit)
        return list(cursor)

    async def insert_crime(self, crime_data: dict) -> dict:
        col = self._get_collection()
        res = col.insert_one(crime_data)
        if hasattr(res, "__await__"):
            await res
        return crime_data

    async def insert_bulk_crimes(self, crimes: list):
        col = self._get_collection()
        if not crimes:
            return
        res = col.insert_many(crimes)
        if hasattr(res, "__await__"):
            await res

class AuditRepository(BaseRepository):
    def __init__(self):
        super().__init__("audit_logs")

    async def log_action(self, username: str, action: str, details: str):
        col = self._get_collection()
        log = {
            "username": username,
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow()
        }
        res = col.insert_one(log)
        if hasattr(res, "__await__"):
            await res
        return log

    async def get_logs(self, limit: int = 20) -> list:
        col = self._get_collection()
        cursor = col.find().sort("timestamp", -1).limit(limit)
        if hasattr(cursor, "to_list"):
            return await cursor.to_list(length=limit)
        return list(cursor)
