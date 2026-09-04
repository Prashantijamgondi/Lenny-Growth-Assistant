import os
import glob
import asyncio
import re
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession

# Need to add this path to allow script to run independently
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal, engine
from app.models.db_models import TranscriptChunk
from app.config import settings

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "lennys-podcast-transcripts")

# Initialize embedding model locally
print(f"Loading embedding model: {settings.EMBEDDING_MODEL}...")
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
print("Model loaded.")

def parse_filename(filename: str) -> Dict[str, str]:
    """Extract episode title and guest from filename heuristically."""
    # Example format might vary, assuming a fallback if we can't parse easily
    base = os.path.basename(filename).replace(".md", "").replace(".txt", "")
    parts = base.split(" with ")
    guest = "Unknown"
    title = base
    if len(parts) == 2:
        title = parts[0].strip()
        guest = parts[1].strip()
    return {"episode": title, "guest": guest}

async def init_db():
    from app.models.db_models import Base
    async with engine.begin() as conn:
        # We assume pgvector extension is already created in the DB manually or via docker-compose init
        await conn.run_sync(Base.metadata.create_all)

async def ingest_transcripts():
    await init_db()
    
    if not os.path.exists(TRANSCRIPTS_DIR):
        print(f"Directory not found: {TRANSCRIPTS_DIR}. Run download_transcripts.py first.")
        return

    files = glob.glob(os.path.join(TRANSCRIPTS_DIR, "**", "*.md"), recursive=True)
    if not files:
        files = glob.glob(os.path.join(TRANSCRIPTS_DIR, "**", "*.txt"), recursive=True)
        
    print(f"Found {len(files)} transcripts to process.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    from sqlalchemy import text
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT DISTINCT episode_title FROM transcript_chunks"))
        existing_episodes = {row[0] for row in result.fetchall()}
        print(f"Found {len(existing_episodes)} existing episodes in database. Will skip these.")

    for file_path in files:
        meta = parse_filename(file_path)
        if meta['episode'] in existing_episodes:
            print(f"Skipping {meta['episode']}, already ingested.")
            continue
            
        print(f"Processing: {meta['episode']}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        chunks = text_splitter.create_documents([content])
        
        # Batch process chunks for embedding
        texts = [c.page_content for c in chunks]
        
        if not texts:
            continue
            
        # Compute embeddings
        embeddings = embedding_model.encode(texts, show_progress_bar=False)
        
        db_chunks = []
        for i, chunk in enumerate(chunks):
            # Basic heuristic for timestamp if present in text
            timestamp = "00:00:00"
            match = re.search(r'\d{2}:\d{2}:\d{2}', chunk.page_content)
            if match:
                timestamp = match.group(0)
            
            db_chunk = TranscriptChunk(
                episode_title=meta['episode'],
                guest_name=meta['guest'],
                chunk_text=chunk.page_content,
                timestamp_ref=timestamp,
                embedding=embeddings[i].tolist()
            )
            db_chunks.append(db_chunk)
            
        # Insert in small batches to avoid network packet timeouts over the internet
        batch_size = 50
        for i in range(0, len(db_chunks), batch_size):
            batch = db_chunks[i:i + batch_size]
            async with AsyncSessionLocal() as session:
                session.add_all(batch)
                await session.commit()
                
        print(f"Inserted {len(db_chunks)} chunks for {meta['episode']}")

    print("Ingestion complete.")

if __name__ == "__main__":
    asyncio.run(ingest_transcripts())
