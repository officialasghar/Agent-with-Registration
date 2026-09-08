from sqlalchemy import Integer, String, Column
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    chat_sessions = relationship("ChatSession", back_populates="user")



