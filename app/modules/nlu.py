import re

# Standard Karnataka Districts and Crime Types for normalization
DISTRICTS = ["Bengaluru", "Mysuru", "Hubballi-Dharwada", "Mangaluru", "Belagavi"]
CRIME_TYPES = ["Cyber Crime", "Theft", "Narcotics", "Crimes Against Women", "Assault"]

def parse_query(query: str) -> dict:
    """
    Parses a natural language user query to classify intent and extract entities
    (Location, Timeframe, Crime Type, IPC Section).
    """
    query_lower = query.lower()
    
    # Initialize response structure
    result = {
        "query": query,
        "intent": "chat_db",  # Default intent
        "entities": {
            "location": None,
            "crime_type": None,
            "time_range": None,
            "days_count": None,
            "ipc_section": None
        }
    }
    
    # 1. INTENT CLASSIFICATION
    if any(k in query_lower for k in ["hotspot", "map", "geospatial", "coordinates", "location of crime", "where did"]):
        result["intent"] = "hotspot_detection"
    elif any(k in query_lower for k in ["predict", "forecast", "future", "warning", "next 30 days", "next month", "trend of next"]):
        result["intent"] = "predictive_forecast"
    elif any(k in query_lower for k in ["network", "gang", "co-offender", "accomplice", "connection", "link", "associate", "partner"]):
        result["intent"] = "network_analysis"
    elif any(k in query_lower for k in ["trend", "rise", "increase", "decrease", "growth", "compare", "monthly change"]):
        result["intent"] = "trend_analysis"
    elif any(k in query_lower for k in ["what is ipc", "explain ipc", "definition", "sop", "procedure", "guideline"]):
        result["intent"] = "general_rag"

    # 2. ENTITY EXTRACTION: Location (Districts)
    for dist in DISTRICTS:
        # Match variations (e.g. Bangalore -> Bengaluru, Mysore -> Mysuru, Hubli -> Hubballi-Dharwada)
        aliases = {
            "Bengaluru": ["bengaluru", "bangalore", "blr"],
            "Mysuru": ["mysuru", "mysore", "mys"],
            "Hubballi-Dharwada": ["hubballi", "hubli", "dharwad", "dharwada", "hubballi-dharwada"],
            "Mangaluru": ["mangaluru", "mangalore", "mlr"],
            "Belagavi": ["belagavi", "belgaum", "bel"]
        }
        for alias in aliases[dist]:
            if re.search(r'\b' + alias + r'\b', query_lower):
                result["entities"]["location"] = dist
                break

    # 3. ENTITY EXTRACTION: Crime Type
    for ct in CRIME_TYPES:
        aliases = {
            "Cyber Crime": ["cyber", "online", "phishing", "scam", "fraud", "hacking"],
            "Theft": ["theft", "steal", "robbery", "stolen", "snatch", "burglary"],
            "Narcotics": ["narcotics", "drug", "ganja", "mdma", "contraband", "peddler"],
            "Crimes Against Women": ["women", "harassment", "molestation", "stalking", "eve-teasing", "domestic violence", "outrage"],
            "Assault": ["assault", "fight", "attack", "beaten", "threat", "violence"]
        }
        for alias in aliases[ct]:
            if re.search(r'\b' + alias + r'\b', query_lower):
                result["entities"]["crime_type"] = ct
                break

    # 4. ENTITY EXTRACTION: IPC Section
    ipc_match = re.search(r'\b(ipc\s*\d+[a-z]?|ndps\s*act|it\s*act)\b', query_lower)
    if ipc_match:
        result["entities"]["ipc_section"] = ipc_match.group(1).upper()
        # If looking up legal codes, default to RAG intent
        if result["intent"] == "chat_db":
            result["intent"] = "general_rag"

    # 5. ENTITY EXTRACTION: Time range / Duration
    # Match patterns like "last 6 months", "30 days", "1 year"
    time_match = re.search(r'\b(last|next)?\s*(\d+)\s*(day|month|year)s?\b', query_lower)
    if time_match:
        direction = time_match.group(1) or "last"
        value = int(time_match.group(2))
        unit = time_match.group(3)
        result["entities"]["time_range"] = f"{direction} {value} {unit}s"
        
        # Calculate days count for internal queries
        multiplier = 1
        if "month" in unit:
            multiplier = 30
        elif "year" in unit:
            multiplier = 365
            
        result["entities"]["days_count"] = value * multiplier

    return result

if __name__ == "__main__":
    # Test cases
    test_queries = [
        "Show crime hotspots in Bangalore last 6 months",
        "Forecast cyber crime incidents for next 30 days in Hubli",
        "Are there any accomplice links for drug peddlers in Mangalore?",
        "Explain penalty under IPC 420",
        "Show me theft trends in Mysore"
    ]
    for q in test_queries:
        print(f"Query: {q}")
        print(parse_query(q))
        print("-" * 50)
