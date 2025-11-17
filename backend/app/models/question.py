from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Question(Base):
    __tablename__ = "Question"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("Challenge.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # Armazena as opções em formato JSON
    correct_answer = Column(String(1), nullable=False)  # 'a', 'b', 'c', 'd', 'e'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Question(id={self.id}, challenge_id={self.challenge_id}, text={self.text[:50]}...)>"
