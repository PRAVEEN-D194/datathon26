from fastapi import APIRouter, Depends
from app.models.schemas import ChatMessage
from app.ai.orchestrator import orchestrate_agents
from app.api.auth import get_current_user

router = APIRouter(prefix="/agents", tags=["AI Agents System"])

@router.post("/orchestrate")
async def orchestrate_chat(payload: ChatMessage, user: dict = Depends(get_current_user)):
    # Personalize response greeting based on user role
    role_prefix = f"[Officer Profile: {user['role'].upper()}] "
    res = await orchestrate_agents(payload.session_id, payload.message)
    res["chatbot_response"] = role_prefix + res["chatbot_response"]
    return res
