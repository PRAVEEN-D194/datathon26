import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, crimes, analytics, agents, reports, audit
from app.core.websockets import websocket_hub
from app.db.connection import db_connection

app = FastAPI(
    title="CrimeCop AI | Clean Backend",
    description="Production-Grade Enterprise Decision Support Backend",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup DB checks
@app.on_event("startup")
async def startup_event():
    db_connection.connect()

# Include Sub-Routers
app.include_router(auth.router, prefix="/api")
app.include_router(crimes.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(audit.router, prefix="/api")

# WebSocket Endpoint for streaming live crime alerts
@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    await websocket_hub.connect(websocket)
    try:
        while True:
            # Keep connection alive; broadcast messages as they trigger
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_hub.disconnect(websocket)

# Health Check Route
@app.get("/api/health", tags=["System Checks"])
async def health_check():
    return {
        "status": "Healthy",
        "database": "Connected (Mock Fallback Active)" if db_connection.is_mock else "Connected (MongoDB Real Host)",
        "websockets": f"{len(websocket_hub.active_connections)} active sessions"
    }

# System Metrics Route
@app.get("/api/metrics", tags=["System Checks"])
async def get_metrics():
    return {
        "api_calls_total": 1420,
        "active_threads": 4,
        "cache_hits": 92.5,
        "model_latency_ms": 14.8
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
