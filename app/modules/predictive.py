import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

DB_PATH = "D:/Datathon - Cyber Nexus/crime_records.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def get_monthly_series(district: str = None, crime_type: str = None):
    """
    Retrieves and aggregates monthly crime counts from the database.
    """
    conn = get_db_connection()
    query = """
        SELECT strftime('%Y-%m', date_occurrence) as month, count(*) as count
        FROM crime_incidents
    """
    filters = []
    if district:
        filters.append(f"district = '{district}'")
    if crime_type:
        filters.append(f"crime_head = '{crime_type}'")
        
    if filters:
        query += " WHERE " + " AND ".join(filters)
        
    query += " GROUP BY month ORDER BY month ASC"
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def forecast_crime_trends(district: str = None, crime_type: str = None, forecast_periods: int = 6):
    """
    Forecasts crime counts for the next N months using a Linear + Seasonal Regression Model.
    Includes explainable parameters.
    """
    df = get_monthly_series(district, crime_type)
    
    if len(df) < 3:
        # Fallback if there isn't enough historical data
        return {
            "history": df.to_dict(orient="records"),
            "forecast": [],
            "explanation": "Insufficient historical data points to fit predictive model."
        }
        
    # Prepare data for regression
    df['index'] = np.arange(len(df))
    
    # Extract seasonal feature (month of the year 0-11)
    df['dt'] = pd.to_datetime(df['month'] + '-01')
    df['month_of_year'] = df['dt'].dt.month
    
    # Simple seasonal encoding
    X = df[['index', 'month_of_year']].values
    y = df['count'].values
    
    # Fit Linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate future periods
    last_idx = df['index'].iloc[-1]
    last_date = df['dt'].iloc[-1]
    
    forecast_records = []
    for i in range(1, forecast_periods + 1):
        future_idx = last_idx + i
        # Calculate future date
        # Handle month rollover
        future_year = last_date.year + (last_date.month + i - 1) // 12
        future_month = (last_date.month + i - 1) % 12 + 1
        future_date_str = f"{future_year}-{future_month:02d}"
        
        pred_val = model.predict([[future_idx, future_month]])[0]
        # Keep predictions positive
        pred_val = max(0, int(round(pred_val)))
        
        forecast_records.append({
            "month": future_date_str,
            "count": pred_val
        })
        
    # Coefficients for explainability
    trend_coeff = model.coef_[0]
    direction = "increasing" if trend_coeff > 0 else "decreasing"
    
    explanation = (
        f"The prediction indicates an overall {direction} trend of approx. "
        f"{abs(trend_coeff):.2f} cases per month. Seasonal weights reflect historical cycles."
    )
    
    return {
        "history": df[['month', 'count']].to_dict(orient="records"),
        "forecast": forecast_records,
        "explanation": explanation
    }

def calculate_district_risk_scores():
    """
    Computes a risk score for each district based on volume and severity of crimes.
    - Cyber Crime & Narcotics carry a weight of 2.0
    - Crimes Against Women & Assault carry a weight of 1.8
    - Theft carries a weight of 1.0
    """
    conn = get_db_connection()
    query = "SELECT district, crime_head, count(*) as count FROM crime_incidents GROUP BY district, crime_head"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    weights = {
        "Cyber Crime": 2.0,
        "Narcotics": 2.0,
        "Crimes Against Women": 1.8,
        "Assault": 1.5,
        "Theft": 1.0
    }
    
    df['weight'] = df['crime_head'].map(weights).fillna(1.0)
    df['weighted_score'] = df['count'] * df['weight']
    
    # Aggregate by district
    scores = df.groupby('district')['weighted_score'].sum().reset_index()
    
    # Scale to 0-100 relative score
    max_score = scores['weighted_score'].max() if not scores.empty else 1
    scores['risk_score'] = ((scores['weighted_score'] / max_score) * 100).round(1)
    
    # Assign risk level
    def get_level(score):
        if score > 80: return "Critical"
        if score > 50: return "High"
        if score > 30: return "Moderate"
        return "Low"
        
    scores['risk_level'] = scores['risk_score'].apply(get_level)
    
    return scores.sort_values(by="risk_score", ascending=False).to_dict(orient="records")

def simulate_crime_scenario(district: str = None, crime_type: str = None, crime_rate_pct_change: float = 0.0, resource_change_pct: float = 0.0):
    """
    Simulates crime volume shifts based on a hypothetical change in base crime rates
    and changes in policing resources.
    - resource_change_pct: Positive percent reduces crime (e.g. +10% resources -> reduces crime by 5%).
    - crime_rate_pct_change: Directly scales the baseline counts.
    """
    # Get standard forecast
    res = forecast_crime_trends(district, crime_type)
    if not res.get("forecast"):
        return res
        
    # Resource efficacy factor: 1% increase in policing resource reduces crime by 0.6%
    net_multiplier = (1.0 + (crime_rate_pct_change / 100.0)) * (1.0 - (resource_change_pct / 100.0 * 0.6))
    
    sim_forecast = []
    for f in res["forecast"]:
        scaled_cnt = max(0, int(round(f["count"] * net_multiplier)))
        sim_forecast.append({
            "month": f["month"],
            "count": scaled_cnt
        })
        
    explanation = (
        f"Scenario simulation results under a {crime_rate_pct_change:+.1f}% crime rate shift "
        f"and {resource_change_pct:+.1f}% police force capacity change. Net projected volume factor: {net_multiplier:.2f}x."
    )
    
    return {
        "history": res["history"],
        "forecast": sim_forecast,
        "explanation": explanation
    }

if __name__ == "__main__":
    print("Testing Forecasting Engine...")
    forecast = forecast_crime_trends("Bengaluru", "Cyber Crime")
    print("Explanation:", forecast["explanation"])
    print("Next 3 forecasted months:", forecast["forecast"][:3])
    
    print("\nTesting Scenario Simulation...")
    sim = simulate_crime_scenario("Bengaluru", "Cyber Crime", 20.0, 10.0)
    print("Simulation Explanation:", sim["explanation"])
    print("Simulated Next 3 months:", sim["forecast"][:3])
    
    print("\nDistrict Risk Scores:")
    for score in calculate_district_risk_scores():
        print(f"- {score['district']}: {score['risk_score']}/100 ({score['risk_level']})")

