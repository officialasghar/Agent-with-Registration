from sqlalchemy.orm import Session
from app.features.chat_management.model import ChatSession, Message
from app.features.agent.services import chat_with_agent
from typing import List, Optional
from app.config import llama_model, gemini_model


###Save User Message to DB
def save_message(db: Session, session_id: int, role: str, content: str):
    msg = Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()


####Generate Title

def generate_chat_title(question: str) -> str:
    # try:
    prompt = (
        "Generate a short chat title for the conversation below, in the style of ChatGPT's "
        "auto-generated conversation titles.\n\n"
        "Rules:\n"
        "- 2 to 4 words maximum\n"
        "- Title Case (capitalize each major word)\n"
        "- Describe the TOPIC or INTENT of the message, not a summary of its content\n"
        "- Do not restate specific facts, numbers, or details from the message\n"
        "- No quotation marks, no punctuation, no trailing period\n"
        "- No generic prefixes like 'Chat about' or 'Title:'\n\n"
        "Examples:\n"
        "User message: 'Hi, I am 25 years old' -> Title: Asking Age\n"
        "User message: 'hello' -> Title: Introduction\n"
        "User message: 'What is the weather in Lahore?' -> Title: Weather Inquiry\n"
        "User message: 'Can you help me write a Python script to scrape a website?' -> Title: Web Scraping Script\n"
        "User message: 'What is 2+2?' -> Title: Simple Math\n\n"
        f"User message: '{question}'\n"
        "Title:"
    )
    response = gemini_model.invoke(prompt)

    title = response.content[0]["text"].strip()
    
    return title if title else "New Chat"

    # except Exception:
    #     # Graceful fallback to prompt snippet if LLM call fails
    #     # return " ".join(question.split()[:5]) or "New Chat"
    #     return "default title"

import uuid
from concurrent.futures import ThreadPoolExecutor

def create_new_chat_session(db: Session, user_id: int, question: str) -> dict:
    # 1. Generate the thread_id ourselves, upfront — no longer dependent on title
    new_thread_id = str(uuid.uuid4())

    # 2. Run title generation and agent response in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        title_future = executor.submit(generate_chat_title, question)
        agent_future = executor.submit(
            chat_with_agent,
            request=question,
            thread_id=new_thread_id,
            user_id=str(user_id)
        )

        generated_title = title_future.result()
        agent_response = agent_future.result()

    response_text = agent_response.get("response", "")

    # 3. NOW create and save the session row, using the same thread_id already used above
    new_session = ChatSession(
        thread_id=new_thread_id,
        title=generated_title,
        user_id=user_id
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # 4. Save both messages
    save_message(db, new_session.id, "user", question)
    save_message(db, new_session.id, "assistant", response_text)

    return {
        "thread_id": new_session.thread_id,
        "title": new_session.title,
        "created_at": new_session.created_at,
        "response": response_text
    }

### Session Retrieval of the current user

def get_user_chat_sessions(db: Session, user_id: int) -> List[ChatSession]:
    """
    Fetches all chat sessions for a given user, ordered from newest to oldest.
    """
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )


###------------------------Saving Chat>> User and Response ---------------------------------

def continue_chat_session(db: Session, user_id: int, thread_id: str, question: str) -> Optional[dict]:
    """
    Continues an existing session: verifies ownership, saves the user's
    message immediately, calls the agent, saves the response immediately.
    """
    session = (
        db.query(ChatSession)
        .filter(ChatSession.thread_id == thread_id, ChatSession.user_id == user_id)
        .first()
    )
    if not session:
        return None

    save_message(db, session.id, "user", question)

    agent_response = chat_with_agent(
        request=question,
        thread_id=thread_id,
        user_id=str(user_id)
    )
    response_text = agent_response.get("response", "")

    save_message(db, session.id, "assistant", response_text)

    return {"response": response_text}


### Get Messages for current session
def get_session_messages(db: Session, user_id: int, thread_id: str) -> Optional[List[Message]]:
    session = (
        db.query(ChatSession)
        .filter(ChatSession.thread_id == thread_id, ChatSession.user_id == user_id)
        .first()
    )
    if not session:
        return None
    return session.messages



###Delete Session and its messages
def delete_chat_session(db: Session, user_id: int, thread_id: str) -> bool:
    """
    Deletes a chat session and all its messages (via cascade).
    Returns True if deleted, False if not found/not owned by this user.
    """
    session = (
        db.query(ChatSession)
        .filter(ChatSession.thread_id == thread_id, ChatSession.user_id == user_id)
        .first()
    )
    if not session:
        return False

    db.delete(session)   # cascade="all, delete-orphan" removes related messages too
    db.commit()
    return True