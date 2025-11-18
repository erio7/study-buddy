from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Question(Base):
    __tablename__ = "Question"
    
    id = Column(Integer, primary_key=True, index=True)
    summary_id = Column(Integer, ForeignKey("Summary.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # Armazena as opções em formato JSON
    correct_answer = Column(String(1), nullable=False)  # 'a', 'b', 'c', 'd', 'e'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Question(id={self.id}, summary_id={self.summary_id}, text={self.text[:50]}...)>"