from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class SummaryCards(BaseModel):
    total_crimes: int
    open_cases: int
    closed_cases: int
    active_alerts: int
    solved_percentage: float

class HotspotPoint(BaseModel):
    latitude: float
    longitude: float
    crime_type: str
    district: str
    weight: float

class DashboardMapData(BaseModel):
    hotspots: List[HotspotPoint]

class ActivityLog(BaseModel):
    id: str
    type: str  # "crime", "alert", "user"
    title: str
    description: str
    timestamp: str
    district: str

class DashboardData(BaseModel):
    summary: SummaryCards
    hotspots: List[HotspotPoint]
    recent_activities: List[ActivityLog]
