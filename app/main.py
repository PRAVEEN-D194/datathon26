import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from app.modules.agent import run_agent_query
from app.modules.predictive import forecast_crime_trends, calculate_district_risk_scores, simulate_crime_scenario
from app.modules.network import analyze_criminal_network
from app.modules.insights import generate_analytical_insights
from app.modules.orchestrator import orchestrate_intelligence_request
from app.modules.reports import generate_html_report
from app.db.database import get_db, CrimeIncident, Offender
from app.modules.ml_models import train_and_save_ml_models, predict_offender_risk, get_kmeans_centroids, detect_isolation_anomalies


app = FastAPI(
    title="CyberNexus | KSP Decision Intelligence Platform",
    description="AI-Powered Decision Intelligence System for Karnataka Police Department",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ForecastRequest(BaseModel):
    district: Optional[str] = None
    crime_type: Optional[str] = None
    periods: Optional[int] = 6

class SimulationRequest(BaseModel):
    district: Optional[str] = "Bengaluru"
    crime_type: Optional[str] = "Cyber Crime"
    crime_rate_pct_change: float = 0.0
    resource_change_pct: float = 0.0

# 1. Master Multi-Agent Orchestrator Endpoint
@app.post("/api/orchestrate")
def orchestrate_endpoint(payload: ChatRequest):
    try:
        response = orchestrate_intelligence_request(payload.session_id, payload.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Conversational Chat Agent Endpoint (Backward compatibility)
@app.post("/api/chat")
def chat_endpoint(payload: ChatRequest):
    try:
        response = run_agent_query(payload.session_id, payload.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Predictive Forecasting & Risks Endpoint
@app.post("/api/predict")
def predict_endpoint(payload: ForecastRequest):
    try:
        forecast_data = forecast_crime_trends(payload.district, payload.crime_type, payload.periods)
        risk_scores = calculate_district_risk_scores()
        return {
            "forecast": forecast_data,
            "risk_scores": risk_scores
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Scenario Simulation Endpoint
@app.post("/api/simulate")
def simulate_endpoint(payload: SimulationRequest):
    try:
        sim_data = simulate_crime_scenario(
            payload.district, 
            payload.crime_type, 
            payload.crime_rate_pct_change, 
            payload.resource_change_pct
        )
        return sim_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Analytical Insights & Anomalies Endpoint
@app.get("/api/insights")
def insights_endpoint():
    try:
        insights = generate_analytical_insights()
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Criminal Link Network Endpoint
@app.get("/api/network")
def network_endpoint():
    try:
        network_data = analyze_criminal_network()
        return network_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. Crime Hotspots Geospatial Coordinates Endpoint
@app.get("/api/hotspots")
def hotspots_endpoint():
    try:
        db_generator = get_db()
        db = next(db_generator)
        incidents = db.query(
            CrimeIncident.incident_id,
            CrimeIncident.district,
            CrimeIncident.station_name,
            CrimeIncident.crime_head,
            CrimeIncident.latitude,
            CrimeIncident.longitude,
            CrimeIncident.status,
            CrimeIncident.date_occurrence
        ).all()
        
        hotspots = [
            {
                "id": inc.incident_id,
                "district": inc.district,
                "station": inc.station_name,
                "type": inc.crime_head,
                "lat": inc.latitude,
                "lng": inc.longitude,
                "status": inc.status,
                "date": inc.date_occurrence.strftime('%Y-%m-%d')
            }
            for inc in incidents
        ]
        return {"hotspots": hotspots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. Report Generator Endpoint
@app.get("/api/report", response_class=HTMLResponse)
def report_endpoint():
    try:
        return generate_html_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. Suspect Profile Facial Similarity Match Mock Endpoint
@app.post("/api/upload_suspect")
def upload_suspect_endpoint(file: UploadFile = File(...)):
    try:
        db_generator = get_db()
        db = next(db_generator)
        # Fetch a random offender to simulate a match
        offender = db.query(Offender).first()
        if not offender:
            return {"match_found": False, "msg": "No suspect files found in KSP registry."}
            
        return {
            "match_found": True,
            "confidence_score": 94.7,
            "suspect": {
                "id": offender.offender_id,
                "name": offender.name,
                "age": offender.age,
                "gender": offender.gender,
                "crime": offender.primary_crime_type,
                "status": "Repeat Offender Registry List"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 10. ML Model Training trigger
@app.post("/api/ml/train")
def train_ml_models_endpoint():
    try:
        logs = train_and_save_ml_models()
        return {"status": "Success", "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 11. K-Means Hotspots centroids
@app.get("/api/ml/clusters")
def get_ml_clusters_endpoint():
    try:
        centroids = get_kmeans_centroids()
        return {"centroids": centroids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 12. Offender Risk Scoring
class RiskScoreRequest(BaseModel):
    age: int
    crime_type: str
    frequency: int
    centrality: float

@app.post("/api/ml/risk_score")
def predict_risk_score_endpoint(payload: RiskScoreRequest):
    try:
        prediction = predict_offender_risk(
            payload.age, 
            payload.crime_type, 
            payload.frequency, 
            payload.centrality
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 13. Isolation Forest Anomalies
@app.get("/api/ml/anomalies")
def get_ml_anomalies_endpoint():
    try:
        anomalies = detect_isolation_anomalies()
        return {"anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount Static Files (the premium demo web app)
static_path = "D:/Datathon - Cyber Nexus/app/static"
os.makedirs(static_path, exist_ok=True)
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
