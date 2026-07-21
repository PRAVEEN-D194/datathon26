from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class GeoLocation(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class VictimInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    demographics: Optional[str] = None

class SuspectInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    criminal_id: Optional[str] = None  # Links to crime_network

class CrimeRecord(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    crime_id: str
    FIR_number: str
    crime_type: str
    crime_category: str
    crime_subcategory: str
    date: datetime
    time: str
    district: str
    police_station: str
    latitude: float
    longitude: float
    victim: VictimInfo
    suspect: SuspectInfo
    status: str  # Under Investigation, Charge-sheeted, Closed
    sections: List[str]
    description: str
    weapon: Optional[str] = None
    vehicle: Optional[str] = None
    location: Optional[GeoLocation] = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "crime_id": "CR-2026-0001",
                "FIR_number": "FIR/2026/001",
                "crime_type": "Theft",
                "crime_category": "Property Crime",
                "crime_subcategory": "Motor Vehicle Theft",
                "date": "2026-07-21T00:00:00",
                "time": "14:30",
                "district": "Bengaluru City",
                "police_station": "Koramangala PS",
                "latitude": 12.9352,
                "longitude": 77.6244,
                "victim": {"name": "Amit Sharma", "age": 34, "gender": "Male"},
                "suspect": {"name": "Ramesh Kumar", "age": 28, "gender": "Male", "criminal_id": "CRIM-002"},
                "status": "Under Investigation",
                "sections": ["379 IPC"],
                "description": "Theft of a blue Honda Activa parked near Koramangala club.",
                "weapon": "None",
                "vehicle": "KA-01-HE-1234",
                "location": {
                    "type": "Point",
                    "coordinates": [77.6244, 12.9352]
                }
            }
        }
    }

class CrimeNetworkConnection(BaseModel):
    criminal_id: str
    relation_type: str
    weight: float

class CrimeNetwork(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    criminal_id: str
    name: str
    connections: List[CrimeNetworkConnection]
    associated_crimes: List[str] = []

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "criminal_id": "CRIM-001",
                "name": "Kiran 'Blade' Kumar",
                "connections": [
                    {"criminal_id": "CRIM-002", "relation_type": "Accomplice", "weight": 0.8},
                    {"criminal_id": "CRIM-003", "relation_type": "Gang Member", "weight": 0.5}
                ],
                "associated_crimes": ["CR-2026-0001", "CR-2026-0012"]
            }
        }
    }

