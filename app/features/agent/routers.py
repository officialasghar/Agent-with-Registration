from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.features.chat_management import service


from app.features.agent.services import chat_with_agent
from app.features.auth.dependencies import get_current_user
from app.features.auth.models import User

from app.features.agent.schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def continue_chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Continues an existing chat session, saves both the user's message
    and the assistant's response to the messages table.
    """
    result = service.continue_chat_session(
        db=db, user_id=current_user.id, thread_id=payload.thread_id, question=payload.question
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return result