from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.schemas import CrimeCreate, CrimeResponse, BulkCrimeUpload
from app.db.repositories import CrimeRepository, AuditRepository
from app.api.auth import get_current_user
import io
import json

router = APIRouter(prefix="/crimes", tags=["Crimes"])
crime_repo = CrimeRepository()
audit_repo = AuditRepository()

@router.get("/", response_model=list[CrimeResponse])
async def list_crimes(
    skip: int = 0, 
    limit: int = 20, 
    district: str = None, 
    crime_type: str = None, 
    user: dict = Depends(get_current_user)
):
    crimes = await crime_repo.get_all_crimes(skip, limit, district, crime_type)
    return crimes

@router.post("/", response_model=CrimeResponse)
async def create_crime(payload: CrimeCreate, user: dict = Depends(get_current_user)):
    crime_dict = payload.dict()
    await crime_repo.insert_crime(crime_dict)
    await audit_repo.log_action(user["username"], "CREATE_CRIME", f"Created incident {payload.incident_id}")
    return crime_dict

@router.post("/bulk-upload")
async def bulk_upload(payload: BulkCrimeUpload, user: dict = Depends(get_current_user)):
    crimes_list = [c.dict() for c in payload.crimes]
    await crime_repo.insert_bulk_crimes(crimes_list)
    await audit_repo.log_action(user["username"], "BULK_UPLOAD", f"Uploaded {len(crimes_list)} incidents")
    return {"status": "Success", "records_inserted": len(crimes_list)}

@router.get("/export/csv")
async def export_crimes_csv(user: dict = Depends(get_current_user)):
    crimes = await crime_repo.get_all_crimes(limit=1000)
    
    output = io.StringIO()
    # Write CSV Header
    output.write("incident_id,district,station_name,crime_head,ipc_sections,latitude,longitude,status\n")
    for c in crimes:
        output.write(f"{c['incident_id']},{c['district']},{c['station_name']},{c['crime_head']},{c['ipc_sections']},{c['latitude']},{c['longitude']},{c['status']}\n")
        
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")), 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=crimes_export.csv"}
    )
