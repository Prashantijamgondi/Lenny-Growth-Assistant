from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid
from typing import List

from app.database import get_db
from app.models.db_models import Session, Message
from app.models.schemas import SessionResponse, SessionCreate, MessageResponse

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])

@router.post("", response_model=SessionResponse)
async def create_session(session_data: SessionCreate, db: AsyncSession = Depends(get_db)):
    db_session = Session(title=session_data.title or "New Chat")
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

@router.get("", response_model=List[SessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).order_by(Session.updated_at.desc()))
    return result.scalars().all()

@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_messages(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message).where(Message.session_id == session_id).order_by(Message.created_at.asc()))
    messages = result.scalars().all()
    return messages
