from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CrimePrediction(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    district: str
    date: datetime
    predicted_crime_count: float
    confidence: float  # e.g., 0.85
    risk_level: str   # Low, Medium, High

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "district": "Bengaluru City",
                "date": "2026-08-01T00:00:00",
                "predicted_crime_count": 142.5,
                "confidence": 0.88,
                "risk_level": "High"
            }
        }
    }
