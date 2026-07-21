from fastapi import APIRouter, Depends
from app.services.analytics import calculate_crime_stats, get_cluster_centroids
from app.api.auth import get_current_user
from app.core.caching import cache

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
async def get_summary(user: dict = Depends(get_current_user)):
    # Check cache first
    cached_res = cache.get("analytics_summary")
    if cached_res:
        return cached_res
        
    res = await calculate_crime_stats()
    cache.set("analytics_summary", res, expire=600)
    return res

@router.get("/clusters")
async def get_clusters(user: dict = Depends(get_current_user)):
    centroids = await get_cluster_centroids()
    return {"centroids": centroids}
