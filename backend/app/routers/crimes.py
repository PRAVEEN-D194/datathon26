from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from datetime import datetime
from app.schemas.crime_schema import CrimeCreate, CrimeUpdate, CrimeResponse
from app.services.crime_service import CrimeService
from app.core.security import RoleChecker

router = APIRouter(prefix="/crimes", tags=["Crime Records"])
crime_service = CrimeService()

@router.post("/", response_model=CrimeResponse, status_code=status.HTTP_201_CREATED)
async def create_new_crime(
    crime_data: CrimeCreate,
    current_user: dict = Depends(RoleChecker(["admin", "officer"]))
):
    # If officer has district constraint, ensure they only add crimes to their district
    if current_user["role"] == "officer" and current_user.get("district"):
        if crime_data.district.lower() != current_user["district"].lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Officers are restricted to filing FIRs within their district: {current_user['district']}"
            )
            
    created = await crime_service.create_crime(crime_data)
    return created

@router.get("/", response_model=List[CrimeResponse])
async def search_crime_records(
    district: Optional[str] = None,
    crime_type: Optional[str] = None,
    police_station: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = None,
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    # Enforce Officer district boundaries
    if current_user["role"] == "officer" and current_user.get("district"):
        district = current_user["district"]
        
    filters = {
        "district": district,
        "crime_type": crime_type,
        "police_station": police_station,
        "status": status,
        "start_date": start_date,
        "end_date": end_date,
        "latitude": latitude,
        "longitude": longitude,
        "radius_km": radius_km
    }
    
    # Filter out empty options
    filters = {k: v for k, v in filters.items() if v is not None}
    return await crime_service.search_crimes(filters, limit, skip)

@router.get("/{crime_id}", response_model=CrimeResponse)
async def get_crime_by_id(
    crime_id: str,
    current_user: dict = Depends(RoleChecker(["admin", "officer", "analyst"]))
):
    crime = await crime_service.get_crime_by_id(crime_id)
    if not crime:
        raise HTTPException(status_code=404, detail="Crime record not found")
        
    # Enforce Officer district boundaries
    if current_user["role"] == "officer" and current_user.get("district"):
        if crime.get("district", "").lower() != current_user["district"].lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Officers are restricted to viewing crimes in their assigned district."
            )
            
    return crime

@router.put("/{crime_id}", response_model=CrimeResponse)
async def update_crime_record(
    crime_id: str,
    update_data: CrimeUpdate,
    current_user: dict = Depends(RoleChecker(["admin", "officer"]))
):
    # Fetch existing to check ownership / permissions
    existing = await crime_service.get_crime_by_id(crime_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Crime record not found")
        
    if current_user["role"] == "officer" and current_user.get("district"):
        if existing.get("district", "").lower() != current_user["district"].lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Officers can only update records belonging to their assigned district."
            )
            
    updated = await crime_service.update_crime(crime_id, update_data.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Update failed")
    return updated

@router.delete("/{crime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crime_record(
    crime_id: str,
    current_user: dict = Depends(RoleChecker(["admin"]))
):
    # Only admin can delete FIR records
    success = await crime_service.delete_crime(crime_id)
    if not success:
        raise HTTPException(status_code=404, detail="Crime record not found")
    return None
