from typing import List, Dict, Any

# Severity weights for crime categories
CRIME_SEVERITY_WEIGHTS = {
    "murder": 10.0,
    "rape": 10.0,
    "kidnapping": 8.0,
    "assault": 6.0,
    "robbery": 7.0,
    "burglary": 5.0,
    "cyber crime": 6.0,
    "theft": 3.0,
    "extortion": 6.0,
    "cheating": 3.0,
    "drug trafficking": 8.0,
    "others": 1.5
}

def calculate_district_risk(
    crimes: List[Dict[str, Any]], 
    district_area_sq_km: float = 1000.0,
    population: int = 500000
) -> Dict[str, Any]:
    """
    Calculate the risk score of a district.
    Returns risk score, risk level, crime density, and seasonal trend.
    """
    if not crimes:
        return {
            "risk_score": 0.0,
            "crime_density": 0.0,
            "seasonal_trend": "Stable",
            "risk_level": "Low"
        }

    total_weighted_score = 0.0
    category_counts = {}

    for crime in crimes:
        c_type = crime.get("crime_type", "others").lower()
        # Find match in weights
        weight = CRIME_SEVERITY_WEIGHTS.get("others")
        for key, val in CRIME_SEVERITY_WEIGHTS.items():
            if key in c_type:
                weight = val
                break
        total_weighted_score += weight
        category_counts[c_type] = category_counts.get(c_type, 0) + 1

    # 1. Crime Density (Weighted crime score per 100,000 population)
    # Using population scaling
    density = (len(crimes) / (population / 100000)) if population > 0 else len(crimes)

    # 2. Risk Score calculation (Normalized between 0 and 100)
    # Base score combines density and severity weights
    base_score = (total_weighted_score / (population / 100000)) if population > 0 else total_weighted_score
    # Cap and scale to 100
    risk_score = min(100.0, max(0.0, base_score * 3.5))

    # 3. Determine Risk Level
    if risk_score >= 70.0:
        risk_level = "High"
    elif risk_score >= 35.0:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # 4. Seasonal Trend analysis (Simple trend projection based on latest timestamps)
    # Group by dates (latest 30 days vs preceding 30 days)
    # If latest count > preceding count -> Increasing
    # If latest count < preceding count -> Decreasing
    # Otherwise -> Stable
    try:
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        latest_30 = 0
        previous_30 = 0
        
        for crime in crimes:
            c_date = crime.get("date")
            if isinstance(c_date, str):
                from app.utils.date_utils import parse_date
                c_date = parse_date(c_date)
            
            if c_date:
                # Localize timezone if comparison is timezone naive
                if c_date.tzinfo is not None:
                    c_date = c_date.replace(tzinfo=None)
                
                if now - c_date <= timedelta(days=30):
                    latest_30 += 1
                elif now - c_date <= timedelta(days=60):
                    previous_30 += 1
                    
        if latest_30 > previous_30 * 1.15:
            seasonal_trend = "Increasing"
        elif latest_30 < previous_30 * 0.85:
            seasonal_trend = "Decreasing"
        else:
            seasonal_trend = "Stable"
    except Exception:
        seasonal_trend = "Stable"

    return {
        "risk_score": round(risk_score, 1),
        "crime_density": round(density, 2),
        "seasonal_trend": seasonal_trend,
        "risk_level": risk_level
    }
