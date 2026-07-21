from typing import Optional, List
from pydantic import BaseModel, Field

class DistrictDetails(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    code: str
    headquarters: str
    population: Optional[int] = None
    area_sq_km: Optional[float] = None
    police_stations_count: int
    coordinates: List[float]  # Central latitude/longitude: [latitude, longitude]

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "Bengaluru City",
                "code": "KA-BC",
                "headquarters": "Bengaluru",
                "population": 8443675,
                "area_sq_km": 709.0,
                "police_stations_count": 108,
                "coordinates": [12.9716, 77.5946]
            }
        }
    }
