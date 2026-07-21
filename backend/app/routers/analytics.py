from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from app.services.analytics_service import AnalyticsService
from app.core.security import RoleChecker

router = APIRouter(prefix="/analytics", tags=["Analytics & Charting"])
analytics_service = AnalyticsService()

@router.get("/trends")
async def get_crime_trends(
    district: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "analyst", "officer"]))
):
    """Get temporal crime count timeline values, formatted for line charts."""
    if current_user["role"] == "officer" and current_user.get("district"):
        district = current_user["district"]
    return await analytics_service.get_crime_trends(district)

@router.get("/hotspots")
async def get_crime_hotspots(
    district: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "analyst", "officer"]))
):
    """Get dense geolocation coordinates of incident hotspots."""
    if current_user["role"] == "officer" and current_user.get("district"):
        district = current_user["district"]
    return await analytics_service.get_crime_hotspots(district)

@router.get("/district")
async def get_district_charts(
    current_user: dict = Depends(RoleChecker(["admin", "analyst", "officer"]))
):
    """Get crime frequency comparison by district."""
    return await analytics_service.get_district_stats()

@router.get("/crime-types")
async def get_crime_types_distribution(
    district: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "analyst", "officer"]))
):
    """Get crime categories distribution proportions, formatted for pie charts."""
    if current_user["role"] == "officer" and current_user.get("district"):
        district = current_user["district"]
    return await analytics_service.get_crime_type_distribution(district)

@router.get("/monthly")
async def get_monthly_distribution(
    district: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "analyst", "officer"]))
):
    """Get crime counts grouped by calendar month."""
    if current_user["role"] == "officer" and current_user.get("district"):
        district = current_user["district"]
    return await analytics_service.get_crime_trends(district)

@router.get("/yearly")
async def get_yearly_distribution(
    district: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "analyst", "officer"]))
):
    """Get historical yearly crime data."""
    if current_user["role"] == "officer" and current_user.get("district"):
        district = current_user["district"]
    return await analytics_service.get_yearly_distribution(district)
