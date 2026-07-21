from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from app.schemas.prediction_schema import ForecastResponse, RiskDetails
from app.services.prediction_service import PredictionService
from app.core.security import RoleChecker

router = APIRouter(prefix="/prediction", tags=["Predictive Analytics"])
prediction_service = PredictionService()

@router.get("/forecast", response_model=ForecastResponse)
async def get_time_series_forecast(
    district: str = Query(..., example="Bengaluru City"),
    months: int = Query(6, ge=1, le=24),
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """
    ARIMA/EMA Time Series forecasting of crime incidence for the specified district.
    """
    return await prediction_service.get_crime_forecast(district, months)

@router.get("/risk", response_model=RiskDetails)
async def get_district_risk_index(
    district: str = Query(..., example="Bengaluru City"),
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """
    Calculates current risk assessment for a district based on crime density and severity.
    """
    return await prediction_service.get_district_risk(district)

@router.get("/top-risk-districts", response_model=List[RiskDetails])
async def get_highest_risk_districts(
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """
    Returns ranking of districts in Karnataka sorted by overall Crime Risk Index.
    """
    return await prediction_service.get_top_risk_districts()
