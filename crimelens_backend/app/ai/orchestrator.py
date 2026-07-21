from app.ai.translation import translate_kannada_to_english, translate_english_to_kannada
from app.ai.nlu import parse_query_nlu
from app.ai.rag import search_rag_context
from app.ai.xai import get_model_explainability_weights
from app.services.analytics import calculate_crime_stats
from app.services.networks import analyze_offender_network

async def orchestrate_agents(session_id: str, raw_query: str) -> dict:
    """
    Master Orchestrator coordinating specialized sub-agents:
    Query Agent, Analytics Agent, Prediction Agent, and Explanation Agent.
    Supports Kannada language detection and translations.
    """
    logs = ["Master Orchestrator initiated."]
    
    # 1. Check Language & Translate
    is_kannada = any(char for char in raw_query if '\u0c80' <= char <= '\u0cff')
    query = raw_query
    if is_kannada:
        logs.append("Kannada script detected. Translating query to English...")
        query = translate_kannada_to_english(raw_query)
        
    # 2. Parse NLU (Intent + Entities)
    parsed = parse_query_nlu(query)
    intent = parsed["intent"]
    entities = parsed["entities"]
    logs.append(f"Intent classified: {intent.upper()} | Location: {entities['location']}")
    
    # 3. Route to specialized sub-agents
    response_text = ""
    visualizations = {}
    
    if intent == "network_analysis":
        logs.append("Routing to Criminal Network Agent...")
        net_data = await analyze_offender_network()
        response_text = net_data["explanation"]
        visualizations["network"] = net_data
        
    elif intent == "trend_analysis":
        logs.append("Routing to Analytics Agent...")
        stats = await calculate_crime_stats()
        response_text = f"Calculated state statistics. Total crimes compiled: {stats['total_crimes']}. Solved percentage is {stats['solved_percentage']}%."
        visualizations["stats"] = stats
        
    elif intent == "predictive_forecast":
        logs.append("Routing to Prediction Agent...")
        response_text = f"Generating crime rate forecast for {entities['crime_type'] or 'Theft'} in {entities['location'] or 'Bengaluru'}."
        
    else:  # Database query / SOP RAG lookup
        logs.append("Routing to RAG Lookup Agent...")
        rag_res = search_rag_context(query)
        if rag_res:
            response_text = f"Document Match: **{rag_res[0]['title']}**\n{rag_res[0]['content']}"
        else:
            response_text = "I searched the KSP guidelines but could not locate a precise SOP match."
            
    # 4. Explainable AI Agent
    logs.append("Generating explainability attribution metrics...")
    xai_weights = get_model_explainability_weights("High")
    
    # 5. Translate response back if input was Kannada
    final_response = response_text
    if is_kannada:
        logs.append("Translating system response back to Kannada...")
        final_response = translate_english_to_kannada(response_text)
        
    return {
        "query": raw_query,
        "is_kannada": is_kannada,
        "chatbot_response": final_response,
        "visualizations": visualizations,
        "xai": xai_weights,
        "agent_logs": logs
    }
