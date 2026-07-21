from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.core.database import get_collection
from app.models.user import User

class UserRepository:
    @staticmethod
    def _to_dict(user: User) -> Dict[str, Any]:
        data = user.model_dump(by_alias=True, exclude_none=True)
        if "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        return data

    @staticmethod
    def _to_model(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if doc is None:
            return None
        doc["_id"] = str(doc["_id"])
        return doc

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        col = get_collection("users")
        doc = await col.find_one({"email": email})
        return self._to_model(doc)

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(user_id):
            return None
        col = get_collection("users")
        doc = await col.find_one({"_id": ObjectId(user_id)})
        return self._to_model(doc)

    async def create(self, user: User) -> Dict[str, Any]:
        col = get_collection("users")
        data = self._to_dict(user)
        res = await col.insert_one(data)
        doc = await col.find_one({"_id": res.inserted_id})
        return self._to_model(doc)

    async def list_all(self) -> List[Dict[str, Any]]:
        col = get_collection("users")
        cursor = col.find()
        users = []
        async for doc in cursor:
            users.append(self._to_model(doc))
        return users

    async def update(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(user_id):
            return None
        col = get_collection("users")
        res = await col.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        if res.modified_count > 0 or res.matched_count > 0:
            doc = await col.find_one({"_id": ObjectId(user_id)})
            return self._to_model(doc)
        return None

    async def delete(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        col = get_collection("users")
        res = await col.delete_one({"_id": ObjectId(user_id)})
        return res.deleted_count > 0
