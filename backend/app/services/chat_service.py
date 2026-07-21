import json
from datetime import datetime
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.crime_service import CrimeService
from app.services.analytics_service import AnalyticsService
from app.services.prediction_service import PredictionService
from app.services.network_service import NetworkService
from app.repositories.chat_repository import ChatRepository
from app.models.chat import ChatMessage
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChartData, MapData, NetworkGraphData, GraphNode, GraphEdge
from app.core.logging import logger

class ChatService:
    def __init__(self):
        self.gemini = GeminiService()
        self.crime_service = CrimeService()
        self.analytics_service = AnalyticsService()
        self.prediction_service = PredictionService()
        self.network_service = NetworkService()
        self.chat_repo = ChatRepository()

    async def handle_chat_message(self, user_id: str, request: ChatRequest) -> ChatResponse:
        """
        Coordinates the AI chatbot workflow.
        """
        message = request.message
        logger.info(f"Processing chatbot message: '{message}' for user {user_id}")

        # 1. Detect Intent and Extract Entities
        analysis = await self.gemini.analyze_query_intent(message)
        intent = analysis.get("intent", "general")
        district = analysis.get("district")
        crime_type = analysis.get("crime_type")
        criminal_id = analysis.get("criminal_id")

        logger.info(f"Extracted Intent: {intent}, District: {district}, Crime Type: {crime_type}, Criminal ID: {criminal_id}")

        # Initialize return items
        answer = ""
        chart = None
        map_data = None
        graph = None
        suggestions = []

        context_data = ""

        # 2. Execute business logic based on intent
        if intent == "search":
            filters = {}
            if district:
                filters["district"] = district
            if crime_type:
                filters["crime_type"] = crime_type
            
            crimes = await self.crime_service.search_crimes(filters, limit=5)
            context_data = f"Search Results for filters {filters}: {str(crimes)}"
            
            # Formulate coordinates for map if available
            coords = []
            for c in crimes:
                if c.get("latitude") and c.get("longitude"):
                    coords.append([c["latitude"], c["longitude"]])
            if coords:
                map_data = MapData(coordinates=coords)

            suggestions = [
                f"Show weekly trends in {district or 'Bengaluru City'}",
                f"Predict crime rates for next 3 months in {district or 'Bengaluru City'}"
            ]

        elif intent == "analytics":
            if crime_type:
                # Distribution of specified crime type
                distribution = await self.analytics_service.get_crime_type_distribution(district)
                chart = ChartData(**distribution)
                context_data = f"Crime type distribution: {str(distribution)}"
            else:
                # Default to temporal trends
                trends = await self.analytics_service.get_crime_trends(district)
                chart = ChartData(**trends)
                context_data = f"Monthly crime trends for district {district or 'all'}: {str(trends)}"

            # Add hotspots map coordinates
            hotspots = await self.analytics_service.get_crime_hotspots(district)
            coords = [[h["latitude"], h["longitude"]] for h in hotspots]
            if coords:
                map_data = MapData(coordinates=coords)

            suggestions = [
                f"Predict crime in {district or 'Bengaluru City'}",
                "Identify repeat offenders"
            ]

        elif intent == "prediction":
            target_district = district or "Bengaluru City"
            forecast_res = await self.prediction_service.get_crime_forecast(target_district, months=6)
            
            # Map forecast to chart
            labels = [p.date for p in forecast_res.forecast]
            values = [p.predicted_count for p in forecast_res.forecast]
            chart = ChartData(type="line", labels=labels, values=values)
            
            risk_info = await self.prediction_service.get_district_risk(target_district)
            context_data = f"6-Month Forecast count details: {str(values)}. Risk Info: {str(risk_info)}"
            
            suggestions = [
                f"Show hotspot mapping in {target_district}",
                "Show gang clusters"
            ]

        elif intent == "network":
            # Call network service
            network_res = await self.network_service.get_criminal_network(criminal_id)
            graph = network_res
            
            context_data = f"Criminal Network graph representation: {len(graph.nodes)} nodes, {len(graph.edges)} connections."
            suggestions = [
                "Find most connected criminals",
                "Show gang clusters"
            ]

        else:  # general / fallback
            # Perform vector matching to find contextual crimes
            from app.services.vector_service import vector_service
            similars = vector_service.search_similar(message, top_k=3)
            if similars:
                context_data = f"Similar historic cases found in database description lookup: {[s[0] for s in similars]}"
            else:
                context_data = "No matching specific records found. Conversational greeting."
            
            suggestions = [
                "Show crime hotspots in Bengaluru City",
                "Predict crime forecast in Mysuru"
            ]

        # 3. Request LLM Response Synthesis
        answer = await self.gemini.generate_response_synthesis(message, context_data)

        # 4. Formulate the response object
        response_obj = ChatResponse(
            answer=answer,
            chart=chart,
            map=map_data,
            graph=graph,
            suggestions=suggestions
        )

        # 5. Save in chat history repository
        chat_msg = ChatMessage(
            user_id=user_id,
            question=message,
            response=response_obj.model_dump(exclude_none=True)
        )
        await self.chat_repo.save_message(chat_msg)

        return response_obj
