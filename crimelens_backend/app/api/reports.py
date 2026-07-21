from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from app.services.reports import build_pdf_report_html
from app.api.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/generate", response_class=HTMLResponse)
async def generate_report(user: dict = Depends(get_current_user)):
    html = build_pdf_report_html()
    return html
