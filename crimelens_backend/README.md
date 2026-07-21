# CrimeLens AI | Production-Grade Decision Intelligence Backend

Welcome to the backend engine of **CrimeLens AI**, built for the Karnataka Police Datathon by **Team CyberNexus**. 

This backend adheres to **Clean Architecture** principles, separating API, Core Services, Repositories, and the Multi-Agent AI system.

---

## 🏗️ Architecture Layout

```text
crimelens_backend/
├── app/
│   ├── api/                   # Router Controllers (auth, crimes, analytics, agents, reports)
│   ├── core/                  # Security (JWT), caching, config, websockets
│   ├── db/                    # DB connection (MongoDB/Motor) & Repositories
│   ├── models/                # Pydantic data contracts
│   ├── services/              # Business Logic (analytics aggregates, networks, reports)
│   └── ai/                    # Multi-Agent orchestrator, translation, RAG, XAI
├── Dockerfile                 # Multi-stage docker build
├── docker-compose.yml         # Compose orchestration stack
└── requirements.txt           # Package requirements
```

---

## ⚡ Key Highlights & Enterprise Features

* **Multi-Agent Orchestrator**: Specialized sub-agents (Query, Analytics, Prediction, and Explanation) aggregated dynamically.
* **Geospatial & Trend Analytics**: Async pipelines calculating district density hotspots and Louvain NetworkX crime syndicate clusters.
* **Real-time Alerting**: WebSockets interface streaming live spike warnings.
* **Dual-Mode Cache & MongoDB**: Graceful fallbacks to memory caches and `mongomock` databases if Redis/MongoDB servers are offline, ensuring instant hackathon demonstration.

---

## 🚀 Setup & Execution Guide

### Option 1: Running via Docker Compose (Recommended)
Launch the entire stack (FastAPI Backend, MongoDB, Redis Cache) with a single command:
```bash
docker-compose up --build
```
The server will boot up and be accessible at:
* **API Documentation (Swagger)**: `http://localhost:8000/docs`
* **Health Check**: `http://localhost:8000/api/health`
* **Real-time Alert Stream**: `ws://localhost:8000/ws/alerts`

### Option 2: Running Locally (Python Environment)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the uvicorn server:
   ```bash
   python main.py
   ```
   *(Toggles to mock MongoDB and memory-cache automatically if external servers are unreachable)*
