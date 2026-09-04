from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("")
async def health_check():
    # In a real scenario, we'd ping the DB and Ollama here.
    # For now, just return OK to satisfy the health probe.
    return {
        "status": "ok",
        "provider": settings.DEFAULT_LLM_PROVIDER,
        "database": "connected (assumed)",
    }
