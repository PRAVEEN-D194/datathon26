from app.modules.nlu import parse_query
from app.modules.agent import run_agent_query
from app.modules.insights import generate_analytical_insights
from app.modules.predictive import forecast_crime_trends
from app.modules.network import analyze_criminal_network
from app.modules.recommender import generate_recommendations

def orchestrate_intelligence_request(session_id: str, query: str) -> dict:
    """
    Master Orchestrator agent that analyzes query intent using NLU, 
    routes it to the correct specialist agents, and aggregates results.
    """
    # 1. NLU Agent - Parsing
    parsed = parse_query(query)
    intent = parsed["intent"]
    entities = parsed["entities"]
    
    # Initialize aggregated payload
    result = {
        "query": query,
        "primary_agent": None,
        "intent": intent,
        "entities": entities,
        "chatbot_response": "",
        "visualizations": {},
        "recommendations": [],
        "agent_logs": []
    }
    
    # 2. Route to specialist agents based on intent
    if intent == "hotspot_detection":
        result["primary_agent"] = "Geospatial Visualization Agent"
        result["agent_logs"].append("Delegating mapping and coordinate plotting to Geospatial Agent.")
        
        # Fetch mock recommendations for hotspots
        loc = entities["location"] or "Bengaluru"
        crime = entities["crime_type"] or "Theft"
        result["recommendations"] = generate_recommendations(loc, crime, "High Surge Alert")
        
        # General response
        result["chatbot_response"] = f"Generating interactive crime hotspots mapping for {loc} location."
        
    elif intent == "predictive_forecast":
        result["primary_agent"] = "Prediction Forecasting Agent"
        result["agent_logs"].append("Delegating time-series regression modelling to Predictive Agent.")
        
        loc = entities["location"] or "Bengaluru"
        crime = entities["crime_type"] or "Cyber Crime"
        forecast_res = forecast_crime_trends(loc, crime, 6)
        
        result["visualizations"]["forecast"] = forecast_res
        result["recommendations"] = generate_recommendations(loc, crime, "Medium")
        result["chatbot_response"] = f"Here is the AI crime count forecast for {crime} in {loc} for the next 6 months:\n\n{forecast_res['explanation']}"
        
    elif intent == "network_analysis":
        result["primary_agent"] = "Criminal Network Link Agent"
        result["agent_logs"].append("Extracting co-offending matrices and gang centrality from NetworkX Agent.")
        
        network_res = analyze_criminal_network()
        result["visualizations"]["network"] = network_res
        result["chatbot_response"] = f"Analyzed criminal linkages. {network_res['explanation']} Total gangs detected: {len(network_res['gangs'])}."
        
    elif intent == "trend_analysis":
        result["primary_agent"] = "Analytical Insights Agent"
        result["agent_logs"].append("Aggregating historical records and calculating growth metrics.")
        
        insights = generate_analytical_insights()
        result["visualizations"]["insights"] = insights
        result["chatbot_response"] = f"Historical crime insights report: {insights['explanation']}"
        
    else:  # chat_db / general_rag
        result["primary_agent"] = "Database Query Agent"
        result["agent_logs"].append("Translating query to SQL schema or retrieving local vector guidelines.")
        
        agent_res = run_agent_query(session_id, query)
        result["chatbot_response"] = agent_res["response"]
        result["visualizations"]["sql"] = agent_res.get("sql")
        result["visualizations"]["data"] = agent_res.get("data")
        result["visualizations"]["columns"] = agent_res.get("columns")
        result["visualizations"]["rag"] = agent_res.get("rag")
        
        # Inject standard recommendation if location is specified
        if entities["location"]:
            result["recommendations"] = generate_recommendations(
                entities["location"], 
                entities["crime_type"] or "Theft"
            )

    return result

if __name__ == "__main__":
    print("Testing Orchestrator...")
    res = orchestrate_intelligence_request("test", "Forecast theft cases in Mysuru")
    print("Primary Agent:", res["primary_agent"])
    print("Response:", res["chatbot_response"])
