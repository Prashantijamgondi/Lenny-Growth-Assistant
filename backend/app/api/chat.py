from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.database import get_db
from app.models.schemas import ChatRequest
from app.models.db_models import Message
from app.rag.retriever import TranscriptRetriever
from app.providers.ollama_provider import OllamaProvider
from app.providers.cloud_provider import ClaudeProvider
from app.skills.ship30_writer import build_ship30_prompt
from app.config import settings

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("")
async def stream_chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    retriever = TranscriptRetriever(db)
    
    # Select model provider dynamically
    provider_name = req.provider or settings.DEFAULT_LLM_PROVIDER
    if provider_name == "claude":
        llm = ClaudeProvider()
    else:
        llm = OllamaProvider()

    async def token_event_generator():
        yield "data: {\"type\": \"status\", \"content\": \"Retrieving transcripts...\"}\n\n"
        
        # 1. Retrieve knowledge
        chunks = await retriever.retrieve_relevant_chunks(req.message)
        
        sources_payload = [
            {"episode": c["episode"], "guest": c["guest"], "timestamp": c["timestamp"], "score": c["score"]}
            for c in chunks
        ]
        
        yield f"data: {{\"type\": \"sources\", \"content\": {json.dumps(sources_payload)}}}\n\n"

        if req.mode == "ship30":
            system_prompt = build_ship30_prompt(req.message, chunks)
            messages = []
        else:
            system_prompt = "You are the Lenny Growth Assistant. Ground every answer in the transcript context provided below. If you cannot answer based on context, state that clearly."
            if chunks:
                context_str = "\n\n".join([
                    f"--- Episode: {c['episode']} (Guest: {c['guest']}) ---\n{c['text']}"
                    for c in chunks
                ])
                system_prompt += f"\n\nContext:\n{context_str}"
            else:
                system_prompt += "\n\nContext: None found."
            
            # Fetch history here if needed, keeping it simple for the SSE payload
            messages = [{"role": "user", "content": req.message}]

        full_response = ""
        
        # Stream model response tokens
        async for token in llm.generate_response(messages, system_prompt):
            full_response += token
            yield f"data: {{\"type\": \"token\", \"content\": {json.dumps(token)}}}\n\n"

        # Save to DB asynchronously after streaming completes
        user_message = Message(session_id=req.session_id, role="user", content=req.message)
        assistant_message = Message(session_id=req.session_id, role="assistant", content=full_response, sources=sources_payload)
        db.add(user_message)
        db.add(assistant_message)
        await db.commit()

        yield "data: [DONE]\n\n"

    return StreamingResponse(token_event_generator(), media_type="text/event-stream")
