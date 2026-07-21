from fastapi import APIRouter, Depends, HTTPException, status
from app.db.repositories import AuditRepository
from app.api.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin Audits"])
audit_repo = AuditRepository()

@router.get("/audit-logs")
async def get_audit_logs(user: dict = Depends(get_current_user)):
    # Restrict to admin role
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden. Administrative access required."
        )
    logs = await audit_repo.get_logs()
    # Serialize datetime to string for json compatibility
    for log in logs:
        if "_id" in log:
            log["_id"] = str(log["_id"])
        if "timestamp" in log:
            log["timestamp"] = log["timestamp"].strftime('%Y-%m-%d %H:%M:%S')
    return {"audit_logs": logs}
