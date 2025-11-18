from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class TestResult(Base):
    __tablename__ = "TestResult"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    summary_id = Column(Integer, ForeignKey("Summary.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)  # 0-100
    correct_count = Column(Integer, nullable=False)
    total_count = Column(Integer, nullable=False)
    time_spent = Column(Integer, nullable=True)  # Tempo em minutos
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relacionamento com respostas
    answers = relationship("Answer", back_populates="test_result", cascade="all, delete-orphan", foreign_keys="[Answer.test_result_id]")
    
    def __repr__(self):
        return f"<TestResult(id={self.id}, user_id={self.user_id}, score={self.score})>"


class Answer(Base):
    __tablename__ = "Answer"
    __table_args__ = (
        UniqueConstraint("test_result_id", "question_id", name="uq_test_question"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    test_result_id = Column(Integer, ForeignKey("TestResult.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("Question.id", ondelete="CASCADE"), nullable=False)
    user_answer = Column(String(1), nullable=False)  # 'a', 'b', 'c', 'd', 'e'
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relacionamento com TestResult
    test_result = relationship("TestResult", back_populates="answers")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, test_result_id={self.test_result_id}, is_correct={self.is_correct})>"
