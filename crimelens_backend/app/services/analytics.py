import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from app.db.connection import get_db

async def calculate_crime_stats():
    """
    Computes aggregate metrics from MongoDB.
    """
    db = get_db()
    col = db["crimes"]
    
    # Fetch all records
    cursor = col.find()
    if hasattr(cursor, "to_list"):
        docs = await cursor.to_list(length=5000)
    else:
        docs = list(cursor)
        
    if not docs:
        return {
            "total_crimes": 0,
            "solved_percentage": 0,
            "pending_count": 0,
            "categories": [],
            "anomalies": []
        }
        
    df = pd.DataFrame(docs)
    total = len(df)
    solved = len(df[df["status"] == "Solved"])
    pending = len(df[df["status"] == "Under Investigation"])
    solved_ratio = round((solved / total) * 100, 2)
    
    # Category aggregation
    cats = df["crime_head"].value_counts().reset_index()
    cats.columns = ["crime_head", "count"]
    
    return {
        "total_crimes": total,
        "solved_percentage": solved_ratio,
        "pending_count": pending,
        "categories": cats.to_dict(orient="records")
    }

async def get_cluster_centroids() -> list:
    """
    Fits K-Means clustering on crime coordinates and returns hot spots centroids.
    """
    db = get_db()
    col = db["crimes"]
    
    cursor = col.find({}, {"latitude": 1, "longitude": 1})
    if hasattr(cursor, "to_list"):
        docs = await cursor.to_list(length=5000)
    else:
        docs = list(cursor)
        
    if len(docs) < 5:
        return [{"lat": 12.9716, "lng": 77.5946, "type": "Cluster Center"}]
        
    df = pd.DataFrame(docs)
    kmeans = KMeans(n_clusters=min(5, len(df)), random_state=42, n_init='auto')
    kmeans.fit(df[["latitude", "longitude"]])
    
    centroids = kmeans.cluster_centers_
    return [{"lat": float(c[0]), "lng": float(c[1]), "type": "Cluster Center"} for c in centroids]
