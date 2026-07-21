from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Alert(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    district: str
    message: str
    severity: str  # Critical, Warning, Info
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "district": "Bengaluru City",
                "message": "Spike in vehicle thefts detected in Koramangala over the past 48 hours.",
                "severity": "Warning",
                "createdAt": "2026-07-21T13:00:00"
            }
        }
    }
