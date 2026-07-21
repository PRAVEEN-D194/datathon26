import uuid
from typing import Dict, Any, List

def generate_uuid(prefix: str = "") -> str:
    """Generate a clean unique string identifier."""
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"

def format_mongo_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert _id ObjectId to a string representation in-place."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def format_mongo_list(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert list of docs with ObjectId _id values to string keys."""
    return [format_mongo_id(d) for d in docs if d]
