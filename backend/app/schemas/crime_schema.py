from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.crime import VictimInfo, SuspectInfo, GeoLocation

class CrimeCreate(BaseModel):
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
    status: str = Field("Under Investigation")
    sections: List[str]
    description: str
    weapon: Optional[str] = None
    vehicle: Optional[str] = None

class CrimeUpdate(BaseModel):
    FIR_number: Optional[str] = None
    crime_type: Optional[str] = None
    crime_category: Optional[str] = None
    crime_subcategory: Optional[str] = None
    date: Optional[datetime] = None
    time: Optional[str] = None
    district: Optional[str] = None
    police_station: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    victim: Optional[VictimInfo] = None
    suspect: Optional[SuspectInfo] = None
    status: Optional[str] = None
    sections: Optional[List[str]] = None
    description: Optional[str] = None
    weapon: Optional[str] = None
    vehicle: Optional[str] = None

class CrimeResponse(BaseModel):
    id: str = Field(..., alias="_id")
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
    status: str
    sections: List[str]
    description: str
    weapon: Optional[str] = None
    vehicle: Optional[str] = None
    location: Optional[GeoLocation] = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }
