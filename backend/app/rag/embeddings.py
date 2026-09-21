import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    @classmethod
    async def embed_query(cls, query: str) -> list[float]:
        """
        Generates embeddings using the free HuggingFace Inference API.
        This avoids loading a 600MB+ PyTorch model into RAM, allowing the app 
        to run on Render's 512MB free tier without crashing (OOM).
        """
        api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{settings.EMBEDDING_MODEL}"
        
        # We can optionally use a token if the user adds one to their environment later
        headers = {}
        if hasattr(settings, "HF_TOKEN") and settings.HF_TOKEN:
            headers["Authorization"] = f"Bearer {settings.HF_TOKEN}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    api_url, 
                    headers=headers, 
                    json={"inputs": [query]},
                    timeout=20.0
                )
                response.raise_for_status()
                
                # The API returns a list of lists (one for each input string)
                embeddings = response.json()
                if isinstance(embeddings, list) and len(embeddings) > 0:
                    return embeddings[0]
                
                logger.error(f"Unexpected response format from HF API: {embeddings}")
                return []
                
        except Exception as e:
            logger.error(f"Failed to generate embeddings from API: {e}")
            # Return an empty vector or handle gracefully in production
            return [0.0] * 384  # all-MiniLM-L6-v2 dimension size
