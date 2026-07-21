"""
SurakshaAI - Spatial Analytics Engine
Computes crime hotspots, density maps, station clusters, and GeoJSON features.
Author: Member 4 (Data Engineer & Visualization Specialist)
"""

import os
import pandas as pd
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ksp_crime_dataset.csv")

class SpatialAnalyticsEngine:
    def __init__(self, data_path=DATA_PATH):
        self.data_path = data_path
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
        else:
            self.df = pd.DataFrame()

    def get_hotspots(self, district=None, category=None, time_range_days=180, limit=200):
        """Returns geospatial crime points and intensity scores for heatmaps."""
        if self.df.empty:
            return {"type": "FeatureCollection", "features": []}

        filtered = self.df.copy()

        if district and district.lower() != "all":
            filtered = filtered[filtered["district"].str.lower() == district.lower()]

        if category and category.lower() != "all":
            filtered = filtered[filtered["crime_category"].str.lower() == category.lower()]

        # Filter by recent days
        if time_range_days:
            filtered["incident_date"] = pd.to_datetime(filtered["incident_date"])
            max_date = filtered["incident_date"].max()
            min_date = max_date - pd.Timedelta(days=time_range_days)
            filtered = filtered[filtered["incident_date"] >= min_date]

        # Top N records for performance
        sample_df = filtered.head(limit)

        features = []
        for _, row in sample_df.iterrows():
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row["longitude"]), float(row["latitude"])]
                },
                "properties": {
                    "fir_number": row["fir_number"],
                    "district": row["district"],
                    "police_station": row["police_station"],
                    "category": row["crime_category"],
                    "sub_category": row["sub_category"],
                    "severity": int(row["severity_score"]),
                    "date": str(row["incident_date"]),
                    "status": row["status"],
                    "intensity": float(row["severity_score"]) / 10.0
                }
            }
            features.append(feature)

        # Calculate district centers & intensity summaries
        district_summary = (
            filtered.groupby("district")
            .agg(
                crime_count=("fir_number", "count"),
                avg_severity=("severity_score", "mean"),
                avg_lat=("latitude", "mean"),
                avg_lng=("longitude", "mean")
            )
            .reset_index()
            .to_dict(orient="records")
        )

        return {
            "type": "FeatureCollection",
            "features": features,
            "total_incidents": len(filtered),
            "district_summaries": district_summary
        }

    def get_station_rankings(self, district=None):
        """Ranks police stations by crime density & unresolved cases."""
        if self.df.empty:
            return []

        filtered = self.df.copy()
        if district and district.lower() != "all":
            filtered = filtered[filtered["district"].str.lower() == district.lower()]

        grouped = filtered.groupby(["district", "police_station"]).agg(
            total_cases=("fir_number", "count"),
            pending_cases=("status", lambda x: (x == "Pending").sum()),
            cyber_crimes=("is_cybercrime", "sum"),
            avg_severity=("severity_score", "mean")
        ).reset_index()

        grouped["avg_severity"] = grouped["avg_severity"].round(2)
        grouped = grouped.sort_values(by="total_cases", ascending=False)
        return grouped.head(15).to_dict(orient="records")

spatial_engine = SpatialAnalyticsEngine()
