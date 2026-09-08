from typing import List
from fastapi import APIRouter, Depends, status , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.auth.models import User
from app.features.chat_management import service
from app.features.chat_management.schemas import (
    ChatSessionResponse,
    NewChatRequest,
    NewChatResponse,
    MessageResponse,
)


router = APIRouter(prefix="/chat", tags=["Chat Management"])


@router.post("/new", response_model=NewChatResponse, status_code=status.HTTP_201_CREATED)
def create_and_start_chat(
    payload: NewChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Creates a new chat session thread, sends the first message to the agent,
    and returns the session details along with the bot's response.
    """
    return service.create_new_chat_session(
        db=db,
        user_id=current_user.id,
        question=payload.question,
    )


@router.get(
    "/sessions",
    response_model=List[ChatSessionResponse],
    status_code=status.HTTP_200_OK,
)
def list_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns all past chat sessions for the authenticated user to populate the sidebar.
    """
    return service.get_user_chat_sessions(db=db, user_id=current_user.id)


###-------------------------Session Content Router---------------------------

@router.get("/{thread_id}/messages", response_model=List[MessageResponse], status_code=status.HTTP_200_OK)
def get_chat_messages(
    thread_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    messages = service.get_session_messages(db=db, user_id=current_user.id, thread_id=thread_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return messages


###----------------Delete Session Router---------------------------------
@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_session(
    thread_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Deletes a chat session and all its messages permanently.
    """
    deleted = service.delete_chat_session(db=db, user_id=current_user.id, thread_id=thread_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return None
