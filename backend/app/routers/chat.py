from fastapi import APIRouter, Depends, status
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.security import RoleChecker

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])
chat_service = ChatService()

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_conversation(
    request: ChatRequest,
    current_user: dict = Depends(RoleChecker(["admin", "officer"]))
):
    """
    Intelligent conversational interface for the Karnataka Police Crime Database.
    Accepts natural language queries, detects intent, pulls spatial/analytics, 
    and synthesizes responses.
    """
    user_id = current_user["_id"]
    response = await chat_service.handle_chat_message(user_id, request)
    return response
