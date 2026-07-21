from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from app.core.database import get_collection
from app.services.analytics_service import AnalyticsService
from app.core.security import RoleChecker

router = APIRouter(prefix="/dashboard", tags=["Dashboard Core"])
analytics_service = AnalyticsService()

@router.get("/summary")
async def get_dashboard_summary(
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    """
    Exposes high-level KPI cards (Total crimes, status breakdowns, alerts counts).
    """
    col = get_collection("crime_records")
    alert_col = get_collection("alerts")
    
    # Calculate counts
    total_crimes = await col.count_documents({})
    open_cases = await col.count_documents({"status": "Under Investigation"})
    closed_cases = await col.count_documents({"status": "Closed"})
    active_alerts = await alert_col.count_documents({})
    
    solved_percentage = 0.0
    if total_crimes > 0:
        solved_percentage = round((closed_cases / total_crimes) * 100, 2)
        
    return {
        "total_crimes": total_crimes,
        "open_cases": open_cases,
        "closed_cases": closed_cases,
        "active_alerts": active_alerts,
        "solved_percentage": solved_percentage
    }

@router.get("/map")
async def get_dashboard_map(
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    """
    Returns full geospatial hotspots map points with coordinate values.
    """
    return await analytics_service.get_crime_hotspots()

@router.get("/cards")
async def get_dashboard_cards(
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    """
    Exposes detailed dashboard cards (e.g. top districts, crime types).
    """
    dist_stats = await analytics_service.get_district_stats()
    types_stats = await analytics_service.get_crime_type_distribution()
    return {
        "top_districts": dist_stats,
        "crime_categories": types_stats
    }

@router.get("/activity")
async def get_dashboard_activity(
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    """
    Returns a timeline list of recent activities (latest crime reports, user additions, alerts).
    """
    crime_col = get_collection("crime_records")
    alert_col = get_collection("alerts")
    
    # Fetch 5 latest crimes
    latest_crimes = await crime_col.find().sort("date", -1).limit(5).to_list(length=5)
    # Fetch 5 latest alerts
    latest_alerts = await alert_col.find().sort("createdAt", -1).limit(5).to_list(length=5)
    
    activities = []
    
    for c in latest_crimes:
        activities.append({
            "id": str(c["_id"]),
            "type": "crime",
            "title": f"New FIR Filed: {c.get('FIR_number')}",
            "description": f"Incident of type {c.get('crime_type')} reported in {c.get('police_station')}.",
            "timestamp": c.get("date").isoformat() if isinstance(c.get("date"), datetime) else str(c.get("date")),
            "district": c.get("district")
        })
        
    for a in latest_alerts:
        activities.append({
            "id": str(a["_id"]),
            "type": "alert",
            "title": f"{a.get('severity').upper()} Alert: {a.get('district')}",
            "description": a.get("message"),
            "timestamp": a.get("createdAt").isoformat() if isinstance(a.get("createdAt"), datetime) else str(a.get("createdAt")),
            "district": a.get("district")
        })
        
    # Sort activities by timestamp descending
    activities = sorted(activities, key=lambda x: x["timestamp"], reverse=True)
    return activities[:10]
