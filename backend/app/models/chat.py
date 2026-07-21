from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    question: str
    response: Dict[str, Any]  # The structured chatbot response
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "user_id": "60c72b2f9b1d8e2d48d28e56",
                "question": "Show crime hotspots in Bangalore",
                "response": {
                    "answer": "Crime hotspots are concentrated in Koramangala and Indiranagar.",
                    "chart": {"type": "bar", "labels": ["Koramangala", "Indiranagar"], "values": [45, 30]},
                    "map": {"coordinates": [[12.9352, 77.6244], [12.9718, 77.6412]]},
                    "graph": {"nodes": [], "edges": []},
                    "suggestions": ["Show temporal trends"]
                },
                "timestamp": "2026-07-21T13:00:00"
            }
        }
    }
