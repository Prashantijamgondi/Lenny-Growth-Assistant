import json
from typing import AsyncGenerator, Dict, Any, List
from .base import BaseLLMProvider
from app.config import settings

# This would ideally use the anthropic SDK, but we can implement a mock/stub 
# or use httpx directly if Anthropic key is provided.
# For this project, we'll implement a basic structure that can be easily extended.

class ClaudeProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3) -> AsyncGenerator[str, None]:
        
        if not self.api_key:
            yield "Error: ANTHROPIC_API_KEY is not set."
            return

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=self.api_key)
        
        try:
            # Claude expects messages in a specific format (user/assistant)
            # system prompt is passed separately
            formatted_messages = []
            for m in messages:
                formatted_messages.append({
                    "role": m["role"] if m["role"] in ["user", "assistant"] else "user",
                    "content": m["content"]
                })

            async with client.messages.stream(
                model=self.model,
                max_tokens=2048,
                temperature=temperature,
                system=system_prompt,
                messages=formatted_messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            yield f"Error communicating with Claude: {str(e)}"
