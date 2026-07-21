from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    password: str
    role: str  # admin, officer, analyst
    district: Optional[str] = None
    station: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "Rajesh Kumar",
                "email": "rajesh.kumar@ksp.gov.in",
                "role": "officer",
                "district": "Bengaluru City",
                "station": "Koramangala PS",
                "createdAt": "2026-07-21T13:00:00"
            }
        }
    }
