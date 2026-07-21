-- SurakshaAI: PostgreSQL / PostGIS Database Schema for KSP Crime Database
-- Author: Member 4 (Data Engineer & Visualization Specialist)

CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. Police Stations Table
CREATE TABLE IF NOT EXISTS ksp_police_stations (
    station_id VARCHAR(50) PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    jurisdiction_zone VARCHAR(100),
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    location GEOMETRY(Point, 4326),
    inspector_in_charge VARCHAR(100),
    contact_phone VARCHAR(20)
);

-- 2. Suspects & Criminal Master Table
CREATE TABLE IF NOT EXISTS ksp_suspects (
    suspect_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    alias VARCHAR(100),
    gang_affiliation VARCHAR(100),
    prior_cases_count INT DEFAULT 0,
    risk_level VARCHAR(20) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. FIR Crime Incidents Master Table
CREATE TABLE IF NOT EXISTS ksp_crime_firs (
    fir_number VARCHAR(100) PRIMARY KEY,
    incident_date DATE NOT NULL,
    incident_time TIME NOT NULL,
    district VARCHAR(100) NOT NULL,
    station_id VARCHAR(50) REFERENCES ksp_police_stations(station_id),
    crime_category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100),
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    geom GEOMETRY(Point, 4326),
    severity_score INT CHECK (severity_score BETWEEN 1 AND 10),
    status VARCHAR(50) DEFAULT 'Under Investigation',
    modus_operandi TEXT,
    suspect_id VARCHAR(50) REFERENCES ksp_suspects(suspect_id),
    estimated_loss_inr NUMERIC(12, 2) DEFAULT 0.00,
    is_cybercrime INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Criminal Relationship & Co-Accused Links Table
CREATE TABLE IF NOT EXISTS ksp_criminal_network (
    link_id SERIAL PRIMARY KEY,
    source_suspect_id VARCHAR(50) REFERENCES ksp_suspects(suspect_id),
    target_suspect_id VARCHAR(50) REFERENCES ksp_suspects(suspect_id),
    relationship_type VARCHAR(100) NOT NULL,
    weight INT DEFAULT 1,
    associated_fir VARCHAR(100) REFERENCES ksp_crime_firs(fir_number),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Spatial and Performance Indexes
CREATE INDEX IF NOT EXISTS idx_firs_geom ON ksp_crime_firs USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_firs_district ON ksp_crime_firs(district);
CREATE INDEX IF NOT EXISTS idx_firs_category ON ksp_crime_firs(crime_category);
CREATE INDEX IF NOT EXISTS idx_firs_date ON ksp_crime_firs(incident_date);
CREATE INDEX IF NOT EXISTS idx_network_source ON ksp_criminal_network(source_suspect_id);
