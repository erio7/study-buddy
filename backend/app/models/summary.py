from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Enum, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum


class DifficultyLevel(str, enum.Enum):
    EASY = "Fácil"
    MEDIUM = "Médio"
    HARD = "Difícil"


class Summary(Base):
    __tablename__ = "Summary"
    __table_args__ = (
        UniqueConstraint("user_id", "study_date", name="uq_user_study_date"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("Challenge.id", ondelete="SET NULL"), nullable=True)
    study_date = Column(Date, nullable=False)
    study_time = Column(Integer, nullable=False)  # Tempo em minutos
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    summary_text = Column(Text, nullable=False)
    photo_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relacionamento com objetivos
    objectives = relationship("SummaryObjective", back_populates="summary", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Summary(id={self.id}, user_id={self.user_id}, study_date={self.study_date})>"


class SummaryObjective(Base):
    __tablename__ = "SummaryObjective"
    
    id = Column(Integer, primary_key=True, index=True)
    summary_id = Column(Integer, ForeignKey("Summary.id", ondelete="CASCADE"), nullable=False)
    objective_text = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relacionamento com Summary
    summary = relationship("Summary", back_populates="objectives")
    
    def __repr__(self):
        return f"<SummaryObjective(id={self.id}, objective_text={self.objective_text})>"
