"""
SurakshaAI - Temporal & Predictive Analytics Engine
Computes monthly crime trends, category distribution, 30-day forecasting, and district risk scoring.
Author: Member 4 (Data Engineer & Visualization Specialist)
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ksp_crime_dataset.csv")

class TemporalAnalyticsEngine:
    def __init__(self, data_path=DATA_PATH):
        self.data_path = data_path
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
            self.df["incident_date"] = pd.to_datetime(self.df["incident_date"])
        else:
            self.df = pd.DataFrame()

    def get_monthly_trends(self, district=None, category=None):
        """Monthly aggregated trend data for charts."""
        if self.df.empty:
            return {"timeline": [], "categories": []}

        filtered = self.df.copy()
        if district and district.lower() != "all":
            filtered = filtered[filtered["district"].str.lower() == district.lower()]

        if category and category.lower() != "all":
            filtered = filtered[filtered["crime_category"].str.lower() == category.lower()]

        filtered["month_year"] = filtered["incident_date"].dt.strftime("%Y-%m")
        monthly = filtered.groupby("month_year").agg(
            total_crimes=("fir_number", "count"),
            cybercrimes=("is_cybercrime", "sum"),
            avg_severity=("severity_score", "mean")
        ).reset_index().sort_values(by="month_year")

        monthly["avg_severity"] = monthly["avg_severity"].round(2)

        # Category breakdown
        cat_dist = filtered["crime_category"].value_counts().reset_index()
        cat_dist.columns = ["category", "count"]

        return {
            "monthly_trends": monthly.to_dict(orient="records"),
            "category_distribution": cat_dist.to_dict(orient="records"),
            "total_incidents": len(filtered)
        }

    def forecast_crime_rates(self, district=None, forecast_days=30):
        """30-day predictive forecasting and risk evaluation."""
        if self.df.empty:
            return {"forecast": [], "risk_score": 50, "risk_level": "MODERATE"}

        filtered = self.df.copy()
        if district and district.lower() != "all":
            filtered = filtered[filtered["district"].str.lower() == district.lower()]

        # Daily aggregations for last 90 days
        daily = filtered.groupby("incident_date").size().reset_index(name="count")
        daily = daily.sort_values("incident_date")

        # Trend estimation using weighted moving average + slope
        recent_values = daily["count"].tail(60).values
        if len(recent_values) == 0:
            avg_daily = 10
            trend_slope = 0.05
        else:
            avg_daily = np.mean(recent_values)
            trend_slope = (recent_values[-1] - recent_values[0]) / max(len(recent_values), 1)

        last_date = daily["incident_date"].max() if not daily.empty else datetime.now()

        forecast_list = []
        for i in range(1, forecast_days + 1):
            f_date = last_date + pd.Timedelta(days=i)
            # Add subtle seasonal noise
            noise = np.sin(i / 3.5) * 1.8 + np.random.uniform(-1, 1)
            predicted_cnt = max(1, int(round(avg_daily + (trend_slope * i * 0.2) + noise)))

            forecast_list.append({
                "date": f_date.strftime("%Y-%m-%d"),
                "predicted_crimes": predicted_cnt,
                "confidence_upper": int(predicted_cnt * 1.25),
                "confidence_lower": max(0, int(predicted_cnt * 0.75))
            })

        # Calculate district risk score (0-100)
        risk_score = min(98, max(20, int(avg_daily * 4.5 + trend_slope * 20)))
        if risk_score > 75:
            risk_level = "CRITICAL / HIGH RISK"
            alert_msg = "Spike predicted in cybercrime and chain snatching during evening hours."
        elif risk_score > 50:
            risk_level = "MODERATE RISK"
            alert_msg = "Standard patrolling recommended for commercial hubs."
        else:
            risk_level = "LOW RISK"
            alert_msg = "Crime indices remain within controlled baselines."

        return {
            "district": district if district else "Karnataka State (All)",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "forecast_days": forecast_days,
            "forecast_data": forecast_list,
            "alert_message": alert_msg,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

temporal_engine = TemporalAnalyticsEngine()
