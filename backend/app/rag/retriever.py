from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Dict, Any
from .embeddings import EmbeddingService
from app.config import settings

class TranscriptRetriever:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def retrieve_relevant_chunks(
        self,
        query: str,
        top_k: int = None,
        similarity_threshold: float = None) -> List[Dict[str, Any]]:
        
        top_k = top_k or settings.TOP_K_CHUNKS
        similarity_threshold = similarity_threshold or settings.SIMILARITY_THRESHOLD

        # Compute vector embedding for incoming user query
        query_vector = await EmbeddingService.embed_query(query)

        # pgvector cosine similarity search: (1 - cosine_distance)
        query_stmt = text("""
            SELECT
                episode_title,
                guest_name,
                chunk_text,
                timestamp_ref,
                1 - (embedding <=> :vector::vector) AS similarity_score
            FROM transcript_chunks
            WHERE 1 - (embedding <=> :vector::vector) >= :threshold
            ORDER BY similarity_score DESC
            LIMIT :limit;
        """)

        result = await self.session.execute(
            query_stmt,
            {
                "vector": str(query_vector),
                "threshold": similarity_threshold,
                "limit": top_k
            }
        )

        rows = result.fetchall()
        return [
            {
                "episode": r.episode_title,
                "guest": r.guest_name,
                "text": r.chunk_text,
                "timestamp": r.timestamp_ref,
                "score": float(r.similarity_score)
            }
            for r in rows
        ]
