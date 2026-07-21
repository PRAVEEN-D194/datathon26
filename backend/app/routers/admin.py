from fastapi import APIRouter, Depends, status, HTTPException
from typing import Dict, Any
from app.core.database import get_db, get_collection
from app.core.security import RoleChecker
from app.services.vector_service import vector_service

router = APIRouter(prefix="/admin", tags=["System Administration"])

@router.get("/status")
async def get_system_status(
    current_user: dict = Depends(RoleChecker(["admin"]))
):
    """
    Get backend status, database collections sizes, and indexing details.
    """
    db = get_db()
    
    # Collection counts
    user_count = await db.users.count_documents({})
    crime_count = await db.crime_records.count_documents({})
    chat_count = await db.chat_history.count_documents({})
    alert_count = await db.alerts.count_documents({})
    network_count = await db.crime_network.count_documents({})
    
    # Try fetching mongo server details
    try:
        build_info = await db.command("buildInfo")
        mongo_version = build_info.get("version", "Unknown")
    except Exception:
        mongo_version = "Connected"
        
    return {
        "status": "Healthy",
        "database": {
            "version": mongo_version,
            "counts": {
                "users": user_count,
                "crime_records": crime_count,
                "chat_history": chat_count,
                "alerts": alert_count,
                "crime_network": network_count
            }
        },
        "vector_service": {
            "documents_indexed": len(vector_service.documents),
            "engine_active": vector_service.use_heavy_ml
        }
    }

@router.post("/vector-sync")
async def rebuild_vector_index(
    current_user: dict = Depends(RoleChecker(["admin"]))
):
    """
    Synchronizes historical descriptions from crime database into FAISS memory vectors.
    """
    col = get_collection("crime_records")
    cursor = col.find({}, {"description": 1, "crime_type": 1, "district": 1, "FIR_number": 1})
    crimes = await cursor.to_list(length=2000)
    
    if not crimes:
        return {"status": "Skipped", "message": "No crime records found to index."}
        
    # Re-initialize vector service document buffers
    vector_service.documents = []
    vector_service.embeddings = []
    if vector_service.index and hasattr(vector_service.index, "reset"):
        vector_service.index.reset()
        
    # Index descriptions
    vector_service.add_documents(crimes, text_field="description")
    
    return {
        "status": "Success",
        "message": f"Successfully indexed {len(crimes)} incidents into Vector database search index."
    }
