# 📊 KSP Crime Database - Data Engineering & Visualization Suite

**Role**: Member 4 - Data Engineer & Visualization Specialist  
**Project**: Intelligent Conversational AI & Analytics Platform for Karnataka State Police (KSP)

This repository contains the complete data engineering pipeline, synthetic crime dataset generation scripts, spatial heatmap algorithms, criminal network link engines, time-series forecasting, and database schemas developed for the Karnataka State Police (KSP) Crime Database.

---

## 🎯 Member 4 Responsibilities & Core Deliverables

1. **Crime Dataset Generation & ETL (`scripts/data_generator.py`)**:
   - Synthesizes 5,000+ realistic KSP crime records across 8 key Karnataka districts (Bengaluru City, Mysuru, Hubballi-Dharwad, Mangaluru, Belagavi, etc.) and 1,100+ police station limits.
   - Outputs: `data/ksp_crime_dataset.csv`, `data/ksp_offenders_network.json`, `data/ksp_districts.json`.

2. **Spatial Analytics Engine (`analytics/spatial_engine.py`)**:
   - DBSCAN / density cluster calculation for crime hotspots.
   - GeoJSON feature formatting for Leaflet / Mapbox heatmaps.
   - Police station ranking by unresolved case volume and crime intensity.

3. **Criminal Network & Link Analysis (`analytics/network_engine.py`)**:
   - Co-accused link graph construction (NetworkX data structures).
   - Gang affiliation mapping and repeat offender risk scoring.

4. **Predictive Analytics & Forecasting (`analytics/temporal_engine.py`)**:
   - Monthly crime category breakdown and time-series trend extraction.
   - 30-day ahead crime forecasting and district risk score calculation (0-100 scale).

5. **Explainable AI Engine (`analytics/explainable_ai.py`)**:
   - Transparent justification generator explaining district risk scores and factor weightings.

6. **PostgreSQL / PostGIS Database Schema (`DOCS/DATABASE_SCHEMA.sql`)**:
   - Production SQL DDL schema with spatial indexes (`GIST`), FIR master tables, suspect tables, and network link tables.

---

## 📂 Repository Structure

```
datathon26/
├── analytics/                 # Data Analytics & Visualization Engines
│   ├── explainable_ai.py      # XAI factor justification generator
│   ├── network_engine.py      # Criminal link analysis graph builder
│   ├── spatial_engine.py      # Spatial hotspot GeoJSON engine
│   └── temporal_engine.py     # 30-day forecasting & time-series trends
├── data/                      # KSP Synthetic Datasets
│   ├── ksp_crime_dataset.csv  # 5,000+ crime records with FIR details
│   ├── ksp_districts.json     # Station coordinates & district centroids
│   └── ksp_offenders_network.json # Suspect & gang relationship graph
├── DOCS/
│   └── DATABASE_SCHEMA.sql    # PostgreSQL / PostGIS database DDL
├── scripts/
│   └── data_generator.py      # Synthetic dataset ETL generator
└── README.md
```

---

## 🚀 Quick Execution Guide

### 1. Generate / Refresh KSP Crime Datasets
```bash
python scripts/data_generator.py
```

### 2. Run Analytics Engines via Python
```python
from analytics.spatial_engine import spatial_engine
from analytics.network_engine import network_engine
from analytics.temporal_engine import temporal_engine

# Get Bengaluru crime hotspots GeoJSON
hotspots = spatial_engine.get_hotspots(district="Bengaluru City")

# Get Criminal Link Analysis graph
network = network_engine.get_suspect_network("Ramesh Blade")

# Get 30-Day Crime Forecast & Risk Score
forecast = temporal_engine.forecast_crime_rates(district="Bengaluru City")
```

---

## 🛠️ Push Member 4 Work to GitHub

```bash
git add .
git commit -m "feat(member4): add KSP crime dataset generator, spatial heatmaps, network link graph analysis, 30-day forecasting engines, and PostGIS schema"
git push origin main
```
