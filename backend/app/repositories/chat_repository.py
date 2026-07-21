from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.core.database import get_collection
from app.models.chat import ChatMessage

class ChatRepository:
    @staticmethod
    def _to_dict(msg: ChatMessage) -> Dict[str, Any]:
        data = msg.model_dump(by_alias=True, exclude_none=True)
        if "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        return data

    @staticmethod
    def _to_model(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if doc is None:
            return None
        doc["_id"] = str(doc["_id"])
        return doc

    async def save_message(self, message: ChatMessage) -> Dict[str, Any]:
        col = get_collection("chat_history")
        data = self._to_dict(message)
        res = await col.insert_one(data)
        doc = await col.find_one({"_id": res.inserted_id})
        return self._to_model(doc)

    async def get_history_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        col = get_collection("chat_history")
        cursor = col.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        history = []
        async for doc in cursor:
            history.append(self._to_model(doc))
        # Return in ascending order for conversational interface
        history.reverse()
        return history
