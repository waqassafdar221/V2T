from fastapi import APIRouter, HTTPException
from app.core.config import settings
from pydantic import BaseModel


router = APIRouter()


class ClientRequest(BaseModel):
    """Model for client requests."""
    prompt: str
    client_id: str = "default"


class AIResponse(BaseModel):
    """Model for AI responses."""
    response: str
    model: str
    enabled: bool


@router.post("/api/generate", response_model=AIResponse)
async def generate_response(request: ClientRequest):
    """
    Generate AI response using GPT-5.1-Codex-Max for all clients.
    
    This endpoint uses the configured AI model (GPT-5.1-Codex-Max) when enabled.
    """
    if not settings.enable_gpt_5_1_codex_max:
        raise HTTPException(
            status_code=503,
            detail="GPT-5.1-Codex-Max is currently disabled"
        )
    
    # Placeholder for actual AI integration
    # In a real implementation, you would call the OpenAI API here
    response_text = f"[GPT-5.1-Codex-Max Response] Processed prompt: {request.prompt}"
    
    return AIResponse(
        response=response_text,
        model=settings.gpt_model,
        enabled=settings.enable_gpt_5_1_codex_max
    )


@router.get("/api/config")
async def get_config():
    """Get current AI configuration."""
    return {
        "model": settings.gpt_model,
        "gpt_5_1_codex_max_enabled": settings.enable_gpt_5_1_codex_max,
        "available_for_all_clients": settings.enable_gpt_5_1_codex_max
    }
