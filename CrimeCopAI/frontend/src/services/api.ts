const API_BASE_URL = "http://localhost:8000/api";

export interface ChatPayload {
  message: str;
  session_id: string;
}

export interface SimulationPayload {
  district: string;
  crime_type: string;
  crime_rate_pct_change: number;
  resource_change_pct: number;
}

export interface RiskScorePayload {
  age: number;
  crime_type: string;
  frequency: number;
  centrality: number;
}

class ApiService {
  private getHeaders() {
    const token = localStorage.getItem("access_token");
    return {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
  }

  // --- Auth Endpoints ---
  async login(username: string, password: str) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) throw new Error("Authentication failed");
    return res.json();
  }

  async register(username: string, password: str, role: string = "investigator") {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, role }),
    });
    if (!res.ok) throw new Error("Registration failed");
    return res.json();
  }

  // --- Multi-Agent AI Orchestrator ---
  async orchestrateChat(message: string, sessionId: string = "session_react") {
    const res = await fetch(`${API_BASE_URL}/agents/orchestrate`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    if (!res.ok) throw new Error("AI query orchestration failed");
    return res.json();
  }

  // --- Analytics & Predictions ---
  async getAnalyticsSummary() {
    const res = await fetch(`${API_BASE_URL}/analytics/summary`, {
      method: "GET",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to fetch analytics");
    return res.json();
  }

  async getKMeansClusters() {
    const res = await fetch(`${API_BASE_URL}/analytics/clusters`, {
      method: "GET",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to fetch cluster centroids");
    return res.json();
  }

  async runScenarioSimulation(payload: SimulationPayload) {
    const res = await fetch(`${API_BASE_URL}/simulate`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Simulation failed");
    return res.json();
  }

  // --- Network Linkage Graph ---
  async getCriminalNetwork() {
    const res = await fetch(`${API_BASE_URL}/network`, {
      method: "GET",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to fetch offender linkages");
    return res.json();
  }

  // --- Suspect Match & Risk Scoring ---
  async uploadSuspectMugshot(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    
    const token = localStorage.getItem("access_token");
    const res = await fetch(`${API_BASE_URL}/upload_suspect`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });
    if (!res.ok) throw new Error("Suspect scan failed");
    return res.json();
  }

  async getOffenderRiskScore(payload: RiskScorePayload) {
    const res = await fetch(`${API_BASE_URL}/ml/risk_score`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Risk score calculation failed");
    return res.json();
  }
}

export const api = new ApiService();
