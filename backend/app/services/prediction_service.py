from typing import List, Dict, Any
from datetime import datetime
from app.core.database import get_collection
from app.ml.forecast import forecast_crime_counts
from app.ml.risk_score import calculate_district_risk
from app.schemas.prediction_schema import ForecastResponse, RiskDetails, ForecastPoint

class PredictionService:
    async def get_crime_forecast(self, district: str, months: int = 6) -> ForecastResponse:
        """
        Retrieves historical data for the district and forecasts future months.
        """
        col = get_collection("crime_records")
        cursor = col.find(
            {"district": {"$regex": f"^{district}$", "$options": "i"}},
            {"date": 1}
        )
        
        dates = []
        async for doc in cursor:
            dt = doc.get("date")
            if isinstance(dt, datetime):
                dates.append(dt)
            elif isinstance(dt, str):
                from app.utils.date_utils import parse_date
                try:
                    dates.append(parse_date(dt))
                except Exception:
                    pass
                    
        # Call forecasting ML engine
        forecast = forecast_crime_counts(dates, months)
        return ForecastResponse(district=district, forecast=forecast)

    async def get_district_risk(self, district: str) -> RiskDetails:
        """
        Fetch crime records and compute the risk indices of a district.
        """
        # Fetch district metadata for population/area (if stored)
        dist_col = get_collection("districts")
        dist_meta = await dist_col.find_one({"name": {"$regex": f"^{district}$", "$options": "i"}})
        
        population = 500000
        area = 1000.0
        if dist_meta:
            population = dist_meta.get("population", population)
            area = dist_meta.get("area_sq_km", area)
            
        col = get_collection("crime_records")
        # Fetch crimes in the past 12 months for risk scoring
        cursor = col.find({"district": {"$regex": f"^{district}$", "$options": "i"}})
        crimes = await cursor.to_list(length=5000)
        
        risk_metrics = calculate_district_risk(crimes, area, population)
        
        return RiskDetails(
            district=district,
            risk_score=risk_metrics["risk_score"],
            crime_density=risk_metrics["crime_density"],
            seasonal_trend=risk_metrics["seasonal_trend"],
            risk_level=risk_metrics["risk_level"]
        )

    async def get_top_risk_districts(self) -> List[RiskDetails]:
        """
        Compute risk metrics for all unique districts in the system and rank them.
        """
        col = get_collection("crime_records")
        # Get list of unique districts
        districts = await col.distinct("district")
        
        top_risks = []
        for dist in districts:
            if not dist:
                continue
            risk_info = await self.get_district_risk(dist)
            top_risks.append(risk_info)
            
        # Sort districts by risk score descending
        top_risks = sorted(top_risks, key=lambda x: x.risk_score, reverse=True)
        return top_risks
