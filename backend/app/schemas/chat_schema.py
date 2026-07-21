from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., example="Show crime hotspots in Bangalore")

class ChartData(BaseModel):
    type: str  # line, bar, pie, radar, etc.
    labels: List[str]
    values: List[float]

class MapData(BaseModel):
    coordinates: List[List[float]]  # List of [lat, lon] coordinates

class GraphNode(BaseModel):
    id: str
    label: str
    group: Optional[str] = None
    val: Optional[int] = 1

class GraphEdge(BaseModel):
    source: str
    target: str
    label: Optional[str] = None
    weight: Optional[float] = 1.0

class NetworkGraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class ChatResponse(BaseModel):
    answer: str
    chart: Optional[ChartData] = None
    map: Optional[MapData] = None
    graph: Optional[NetworkGraphData] = None
    suggestions: List[str] = []
