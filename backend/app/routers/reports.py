from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import StreamingResponse, Response
from typing import Dict, Any, Optional
from app.services.report_service import ReportService
from app.repositories.crime_repository import CrimeRepository
from app.core.security import RoleChecker
import io

router = APIRouter(prefix="/reports", tags=["Reports Generation"])
report_service = ReportService()
crime_repo = CrimeRepository()

async def _fetch_filtered_crimes(filters: Dict[str, Any]) -> list:
    """Helper to fetch crimes based on query body filter options."""
    query = {}
    if filters.get("district"):
        query["district"] = filters["district"]
    if filters.get("crime_type"):
        query["crime_type"] = filters["crime_type"]
    if filters.get("status"):
        query["status"] = filters["status"]
        
    return await crime_repo.search(query, limit=500)

@router.post("/pdf")
async def export_pdf_report(
    filters: Dict[str, Any] = Body(...),
    current_user: dict = Depends(RoleChecker(["admin", "officer"]))
):
    """
    Generate and download a styled PDF document of crime records.
    """
    # Enforce Officer district boundaries
    if current_user["role"] == "officer" and current_user.get("district"):
        filters["district"] = current_user["district"]
        
    crimes = await _fetch_filtered_crimes(filters)
    
    title = "CrimeLens AI Incident Report"
    if filters.get("district"):
        title += f" - {filters['district']}"
        
    pdf_bytes = report_service.generate_pdf_report(crimes, title)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=crime_report.pdf"}
    )

@router.post("/export")
async def export_crime_data(
    payload: Dict[str, Any] = Body(...),
    current_user: dict = Depends(RoleChecker(["admin", "officer"]))
):
    """
    Export crime data as CSV, Excel, or PDF based on selected filters and export format.
    Payload Schema:
    {
      "format": "csv" | "excel" | "pdf",
      "filters": { "district": "...", "crime_type": "...", "status": "..." }
    }
    """
    export_format = payload.get("format", "csv").lower()
    filters = payload.get("filters", {})
    
    # Enforce Officer district boundaries
    if current_user["role"] == "officer" and current_user.get("district"):
        filters["district"] = current_user["district"]

    crimes = await _fetch_filtered_crimes(filters)
    
    if export_format == "csv":
        csv_str = report_service.generate_csv_report(crimes)
        return Response(
            content=csv_str,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=crime_export.csv"}
        )
        
    elif export_format == "excel":
        excel_bytes = report_service.generate_excel_report(crimes)
        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=crime_export.xlsx"}
        )
        
    elif export_format == "pdf":
        title = "CrimeLens AI Export Summary"
        if filters.get("district"):
            title += f" - {filters['district']}"
        pdf_bytes = report_service.generate_pdf_report(crimes, title)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=crime_export.pdf"}
        )
        
    else:
        raise HTTPException(status_code=400, detail="Invalid export format. Choose csv, excel, or pdf.")
