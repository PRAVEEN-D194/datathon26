from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from app.schemas.chat_schema import NetworkGraphData
from app.services.network_service import NetworkService
from app.core.security import RoleChecker

router = APIRouter(prefix="/network", tags=["Crime Network Analysis"])
network_service = NetworkService()

@router.get("/gangs")
async def get_gang_clusters(
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """Detects community clusters of active criminal gangs in the database."""
    return await network_service.get_gang_clusters()

@router.get("/repeat-offenders")
async def get_repeat_offenders(
    min_crimes: int = Query(2, ge=2),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """Retrieves offenders linked to multiple active FIRs."""
    return await network_service.get_repeat_offenders(min_crimes, limit)

@router.get("/predict-links")
async def get_accomplice_predictions(
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """Recommends hidden accomplice links using structural graph calculations."""
    return await network_service.get_predicted_links()

@router.get("/{criminal_id}", response_model=NetworkGraphData)
async def get_criminal_connections(
    criminal_id: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """
    Get graph elements (nodes and edges) for a suspect's accomplice network.
    Set criminal_id query to null to fetch the complete network dataset.
    """
    if criminal_id == "all" or criminal_id == "":
        criminal_id = None
    return await network_service.get_criminal_network(criminal_id)
