from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ForecastRequest(BaseModel):
    district: str
    months: int = 6

class ForecastPoint(BaseModel):
    date: str
    predicted_count: float
    confidence_lower: float
    confidence_upper: float

class ForecastResponse(BaseModel):
    district: str
    forecast: List[ForecastPoint]

class RiskDetails(BaseModel):
    district: str
    risk_score: float  # 0 to 100
    crime_density: float  # crimes per sq km or population ratio
    seasonal_trend: str  # Increasing, Decreasing, Stable
    risk_level: str  # Low, Medium, High

class TopRiskDistrictsResponse(BaseModel):
    districts: List[RiskDetails]
