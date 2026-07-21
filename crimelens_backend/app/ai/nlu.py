import re

DISTRICTS = ["Bengaluru", "Mysuru", "Hubballi-Dharwada", "Mangaluru", "Belagavi"]
CRIME_TYPES = ["Cyber Crime", "Theft", "Narcotics", "Crimes Against Women", "Assault"]

def parse_query_nlu(query: str) -> dict:
    query_lower = query.lower()
    
    result = {
        "intent": "chat_db",
        "entities": {
            "location": None,
            "crime_type": None,
            "time_range": None,
            "days_count": None
        }
    }
    
    if any(k in query_lower for k in ["hotspot", "map", "geospatial", "coordinates"]):
        result["intent"] = "hotspot_detection"
    elif any(k in query_lower for k in ["predict", "forecast", "future", "next 30 days"]):
        result["intent"] = "predictive_forecast"
    elif any(k in query_lower for k in ["network", "gang", "co-offender", "accomplice"]):
        result["intent"] = "network_analysis"
    elif any(k in query_lower for k in ["trend", "rise", "increase", "decrease"]):
        result["intent"] = "trend_analysis"
        
    for dist in DISTRICTS:
        aliases = [dist.lower(), dist.lower().split('-')[0]]
        if any(a in query_lower for a in aliases):
            result["entities"]["location"] = dist
            break
            
    for ct in CRIME_TYPES:
        aliases = [ct.lower(), ct.lower().split(' ')[0]]
        if any(a in query_lower for a in aliases):
            result["entities"]["crime_type"] = ct
            break
            
    return result
