from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from app.models.alert import Alert
from app.core.database import get_collection
from app.core.security import RoleChecker

router = APIRouter(prefix="/alerts", tags=["System Alerts"])

@router.get("/", response_model=List[Alert])
async def list_active_alerts(
    district: Optional[str] = None,
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    """
    List active alerts in the state. Can be filtered by district.
    """
    col = get_collection("alerts")
    query = {}
    if district:
        query["district"] = {"$regex": f"^{district}$", "$options": "i"}
        
    cursor = col.find(query).sort("createdAt", -1)
    alerts = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        alerts.append(Alert(**doc))
    return alerts

@router.post("/", response_model=Alert, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: Alert,
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """
    Broadcast a new system alert/warning for a district.
    """
    col = get_collection("alerts")
    data = alert.model_dump(by_alias=True, exclude_none=True)
    if "_id" in data:
        data.pop("_id")
        
    res = await col.insert_one(data)
    doc = await col.find_one({"_id": res.inserted_id})
    doc["_id"] = str(doc["_id"])
    return Alert(**doc)

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: str,
    current_user: dict = Depends(RoleChecker(["admin", "analyst"]))
):
    """
    Dismiss or delete a system alert.
    """
    if not ObjectId.is_valid(alert_id):
        raise HTTPException(status_code=400, detail="Invalid Alert ID format")
        
    col = get_collection("alerts")
    res = await col.delete_one({"_id": ObjectId(alert_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return None
