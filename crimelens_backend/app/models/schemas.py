from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "investigator"  # admin, investigator, analyst

class UserResponse(BaseModel):
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

# --- Crime Schemas ---
class CrimeCreate(BaseModel):
    incident_id: str
    district: str
    station_name: str
    crime_head: str
    ipc_sections: str
    date_occurrence: datetime
    latitude: float
    longitude: float
    status: str = "Under Investigation"
    summary: Optional[str] = None

class CrimeResponse(BaseModel):
    incident_id: str
    district: str
    station_name: str
    crime_head: str
    ipc_sections: str
    date_occurrence: datetime
    latitude: float
    longitude: float
    status: str
    summary: Optional[str]

class BulkCrimeUpload(BaseModel):
    crimes: List[CrimeCreate]

# --- AI Chat / Agent Schemas ---
class ChatMessage(BaseModel):
    message: str
    session_id: str = "default_session"

# --- Simulation Schemas ---
class SimulationParams(BaseModel):
    district: str = "Bengaluru"
    crime_type: str = "Cyber Crime"
    crime_rate_pct_change: float = 0.0
    resource_change_pct: float = 0.0
