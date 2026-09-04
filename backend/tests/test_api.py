import pytest
from app.models.schemas import ChatRequest

def test_chat_request_schema():
    req = ChatRequest(session_id="123e4567-e89b-12d3-a456-426614174000", message="Hello")
    assert req.mode == "default"
    assert req.provider == "ollama"

def test_chat_request_schema_overrides():
    req = ChatRequest(session_id="123e4567-e89b-12d3-a456-426614174000", message="Hello", mode="ship30", provider="claude")
    assert req.mode == "ship30"
    assert req.provider == "claude"
