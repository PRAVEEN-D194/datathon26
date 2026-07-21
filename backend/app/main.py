import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Database, get_collection
from app.core.middleware import RequestLoggingMiddleware
from app.core.logging import logger

# Import all routers
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.chat import router as chat_router
from app.routers.crimes import router as crimes_router
from app.routers.analytics import router as analytics_router
from app.routers.prediction import router as prediction_router
from app.routers.network import router as network_router
from app.routers.dashboard import router as dashboard_router
from app.routers.reports import router as reports_router
from app.routers.alerts import router as alerts_router
from app.routers.admin import router as admin_router

from app.services.vector_service import vector_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing CrimeLens AI application startup...")
    
    # 1. Establish MongoDB connection
    await Database.connect_db()
    
    # 2. Sync vector search cache with historic crime records
    try:
        col = get_collection("crime_records")
        cursor = col.find({}, {"description": 1, "crime_type": 1, "district": 1, "FIR_number": 1})
        crimes = await cursor.to_list(length=1000)
        if crimes:
            vector_service.add_documents(crimes, text_field="description")
            logger.info(f"Loaded {len(crimes)} descriptions into similarity vector engine.")
        else:
            logger.info("No crime records found during startup vector sync.")
    except Exception as e:
        logger.error(f"Vector database warmup failed: {e}")
        
    yield
    
    # Shutdown actions
    logger.info("Tearing down CrimeLens AI application...")
    await Database.close_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Conversational AI Platform and Predictive Analytics Engine for the Karnataka Police Crime Database.",
    version="1.0.0",
    lifespan=lifespan
)

# 1. Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Add Request logging & Rate Limiter
app.add_middleware(RequestLoggingMiddleware)

# 3. Include API Route endpoints
api_prefix = "/api"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(chat_router, prefix=api_prefix)
app.include_router(crimes_router, prefix=api_prefix)
app.include_router(analytics_router, prefix=api_prefix)
app.include_router(prediction_router, prefix=api_prefix)
app.include_router(network_router, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)
app.include_router(alerts_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)

# 4. Status Checks
@app.get("/", tags=["Status"])
async def root_health_check():
    return {
        "app": settings.PROJECT_NAME,
        "environment": settings.ENV,
        "status": "Running",
        "api_docs": "/docs"
    }

# 5. Global Exception Interceptor
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error encountered: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal system error occurred. Please contact the administrator."}
    )
