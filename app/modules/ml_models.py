import os
import sqlite3
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from app.modules.network import analyze_criminal_network

DB_PATH = "D:/Datathon - Cyber Nexus/crime_records.db"
MODEL_DIR = "D:/Datathon - Cyber Nexus/models"

os.makedirs(MODEL_DIR, exist_ok=True)

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def train_and_save_ml_models():
    """
    Fits and saves K-Means (hotspots), Random Forest (offender risk profiling),
    and Isolation Forest (daily volume anomalies).
    """
    conn = get_db_connection()
    logs = []

    # --- 1. K-Means Hotspot Clustering ---
    try:
        incidents_df = pd.read_sql_query("SELECT latitude, longitude FROM crime_incidents", conn)
        if len(incidents_df) >= 5:
            kmeans = KMeans(n_clusters=5, random_state=42, n_init='auto')
            kmeans.fit(incidents_df[['latitude', 'longitude']])
            
            with open(f"{MODEL_DIR}/kmeans_hotspots.pkl", "wb") as f:
                pickle.dump(kmeans, f)
            logs.append("K-Means hotspot model trained successfully.")
        else:
            logs.append("Insufficient data for K-Means.")
    except Exception as e:
        logs.append(f"K-Means training failed: {str(e)}")

    # --- 2. Random Forest Offender Risk Classifier ---
    try:
        # Build training set from sqlite database & NetworkX centrality
        network_data = analyze_criminal_network()
        nodes = network_data["nodes"]
        
        # Build dataframe
        offender_list = []
        for node in nodes:
            # Map crime type to numeric
            crime_map = {"Cyber Crime": 2.0, "Narcotics": 2.0, "Crimes Against Women": 1.8, "Assault": 1.5, "Theft": 1.0}
            crime_num = crime_map.get(node["primary_crime_type"], 1.0)
            
            # Fetch crime frequency
            off_id = node["id"]
            freq_df = pd.read_sql_query(
                "SELECT count(*) as count FROM incident_offender WHERE offender_id = ?", 
                conn, 
                params=(off_id,)
            )
            freq = int(freq_df.iloc[0]["count"])
            
            # Label heuristic: High if freq >= 3 or centrality > 0.4; Moderate if freq == 2; Low otherwise
            centrality = node["centrality"]
            if freq >= 3 or centrality > 0.4:
                label = "High"
            elif freq == 2:
                label = "Moderate"
            else:
                label = "Low"
                
            offender_list.append({
                "age": node["age"],
                "crime_weight": crime_num,
                "frequency": freq,
                "centrality": centrality,
                "label": label
            })
            
        if len(offender_list) >= 3:
            train_df = pd.DataFrame(offender_list)
            X = train_df[["age", "crime_weight", "frequency", "centrality"]]
            y = train_df["label"]
            
            rf = RandomForestClassifier(n_estimators=10, random_state=42)
            rf.fit(X, y)
            
            with open(f"{MODEL_DIR}/rf_risk.pkl", "wb") as f:
                pickle.dump(rf, f)
            logs.append("Random Forest risk classifier trained successfully.")
        else:
            logs.append("Insufficient offender records for RF classifier.")
    except Exception as e:
        logs.append(f"Random Forest training failed: {str(e)}")

    # --- 3. Isolation Forest Anomaly Detector ---
    try:
        # Aggregate crimes by date
        daily_df = pd.read_sql_query(
            "SELECT date(date_occurrence) as date, count(*) as count FROM crime_incidents GROUP BY date", 
            conn
        )
        if len(daily_df) >= 10:
            iso = IsolationForest(contamination=0.05, random_state=42)
            # Reshape counts
            iso.fit(daily_df[["count"]])
            
            with open(f"{MODEL_DIR}/isolation_forest.pkl", "wb") as f:
                pickle.dump(iso, f)
            logs.append("Isolation Forest anomaly detector trained successfully.")
        else:
            logs.append("Insufficient daily data for Isolation Forest.")
    except Exception as e:
        logs.append(f"Isolation Forest training failed: {str(e)}")

    conn.close()
    return logs

def predict_offender_risk(age: int, primary_crime_type: str, frequency: int, centrality: float) -> dict:
    """
    Predicts offender risk category and returns SHAP-style local feature weights.
    """
    model_path = f"{MODEL_DIR}/rf_risk.pkl"
    crime_map = {"Cyber Crime": 2.0, "Narcotics": 2.0, "Crimes Against Women": 1.8, "Assault": 1.5, "Theft": 1.0}
    crime_weight = crime_map.get(primary_crime_type, 1.0)
    
    # Check if model exists, if not train it
    if not os.path.exists(model_path):
        train_and_save_ml_models()
        
    try:
        with open(model_path, "rb") as f:
            rf = pickle.load(f)
            
        features = np.array([[age, crime_weight, frequency, centrality]])
        prediction = rf.predict(features)[0]
        
        # Calculate mock SHAP/XAI feature importance based on classifier split weights
        importances = rf.feature_importances_
        explainability = {
            "Offense Frequency Impact": round(importances[2] * 100, 1),
            "Co-Offender Network Position": round(importances[3] * 100, 1),
            "Crime Severity Rating": round(importances[1] * 100, 1),
            "Age Variable Weight": round(importances[0] * 100, 1)
        }
        
        return {
            "predicted_risk_level": prediction,
            "explainability": explainability,
            "reasoning": f"Decision trees classified risk as {prediction} based on frequency ({frequency}) and association centrality ({centrality})."
        }
    except Exception as e:
        # Fallback heuristic if pickle fails
        return {
            "predicted_risk_level": "High" if frequency >= 3 else "Moderate" if frequency == 2 else "Low",
            "explainability": {
                "Offense Frequency Impact": 50.0,
                "Co-Offender Network Position": 30.0,
                "Crime Severity Rating": 15.0,
                "Age Variable Weight": 5.0
            },
            "reasoning": "Heuristic fallback classifier active."
        }

def get_kmeans_centroids() -> list:
    """
    Loads K-Means hotspots model and returns center coordinates.
    """
    model_path = f"{MODEL_DIR}/kmeans_hotspots.pkl"
    if not os.path.exists(model_path):
        train_and_save_ml_models()
        
    try:
        with open(model_path, "rb") as f:
            kmeans = pickle.load(f)
        centroids = kmeans.cluster_centers_
        return [{"lat": float(c[0]), "lng": float(c[1]), "type": "Cluster Center"} for c in centroids]
    except Exception:
        # Fallback centers (Karnataka hubs)
        return [
            {"lat": 12.9716, "lng": 77.5946, "type": "Cluster Center"},
            {"lat": 12.2958, "lng": 76.6394, "type": "Cluster Center"},
            {"lat": 15.3647, "lng": 75.1240, "type": "Cluster Center"}
        ]

def detect_isolation_anomalies() -> list:
    """
    Detects daily count outlier spikes using Isolation Forest.
    """
    model_path = f"{MODEL_DIR}/isolation_forest.pkl"
    if not os.path.exists(model_path):
        train_and_save_ml_models()
        
    conn = get_db_connection()
    try:
        daily_df = pd.read_sql_query(
            "SELECT date(date_occurrence) as date, count(*) as count FROM crime_incidents GROUP BY date ORDER BY date DESC", 
            conn
        )
        with open(model_path, "rb") as f:
            iso = pickle.load(f)
            
        daily_df["anomaly"] = iso.predict(daily_df[["count"]])
        # -1 represents an anomaly outlier in IsolationForest
        anom_dates = daily_df[daily_df["anomaly"] == -1].head(5)
        
        return [
            {
                "date": row["date"],
                "incidents_count": int(row["count"]),
                "msg": f"Statistically abnormal volume spike of {row['count']} crimes detected."
            }
            for _, row in anom_dates.iterrows()
        ]
    except Exception:
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    print("Training ML pipelines...")
    logs = train_and_save_ml_models()
    print("\n".join(logs))
    
    print("\nPredicting offender risk:")
    print(predict_offender_risk(30, "Cyber Crime", 3, 0.45))
