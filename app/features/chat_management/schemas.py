from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel


class NewChatRequest(BaseModel):
    question: str

class ChatSessionResponse(BaseModel):
    id: int
    thread_id: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class NewChatResponse(BaseModel):
    thread_id: str
    title: str
    created_at: datetime
    response: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True