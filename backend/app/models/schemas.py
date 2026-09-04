from pydantic import BaseModel, UUID4
from typing import List, Optional, Any
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    role: str = "user"

class ChatRequest(BaseModel):
    session_id: str
    message: str
    mode: Optional[str] = "default"  # "default" or "ship30"
    provider: Optional[str] = "ollama"  # "ollama" or "claude"

class MessageResponse(BaseModel):
    id: UUID4
    session_id: UUID4
    role: str
    content: str
    sources: Optional[List[Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: UUID4
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    title: Optional[str] = None
