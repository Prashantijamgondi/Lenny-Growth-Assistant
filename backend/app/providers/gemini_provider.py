import json
from typing import AsyncGenerator, Dict, Any, List
from .base import BaseLLMProvider
from app.config import settings

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or getattr(settings, "GEMINI_API_KEY", None)
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3) -> AsyncGenerator[str, None]:
        
        if not self.api_key:
            yield "Error: GEMINI_API_KEY is not set."
            return

        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            # Convert messages to Gemini format
            contents = []
            for m in messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=m["content"])])
                )

            # Gemini expects system prompt in config
            config = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_prompt,
            )

            # Note: google-genai's stream is synchronous or asynchronous depending on client
            response = await client.aio.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=config,
            )
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            yield f"Error communicating with Gemini: {str(e)}"
