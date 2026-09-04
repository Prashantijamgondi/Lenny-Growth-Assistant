from sentence_transformers import SentenceTransformer
from app.config import settings

class EmbeddingService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print(f"Loading embedding model: {settings.EMBEDDING_MODEL}...")
            cls._instance = SentenceTransformer(settings.EMBEDDING_MODEL)
            print("Model loaded.")
        return cls._instance

    @classmethod
    async def embed_query(cls, query: str) -> list[float]:
        # Since it's a CPU-bound sync operation, ideally this would run in a threadpool
        # But for this assignment, we can just call it synchronously
        model = cls.get_instance()
        embedding = model.encode([query], show_progress_bar=False)[0]
        return embedding.tolist()
