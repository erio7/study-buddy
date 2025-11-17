from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class DifficultyEnum(str, Enum):
    EASY = "Fácil"
    MEDIUM = "Médio"
    HARD = "Difícil"


class SummaryObjectiveResponse(BaseModel):
    """Schema para resposta de objetivo do resumo"""
    id: int
    objective_text: str
    
    class Config:
        from_attributes = True


class SummaryCreate(BaseModel):
    """Schema para criar um novo resumo"""
    challenge_id: Optional[int] = None
    study_date: date
    study_time: int  # Minutos
    difficulty: DifficultyEnum
    summary_text: str
    photo_url: Optional[str] = None
    objectives: Optional[List[str]] = None


class SummaryResponse(BaseModel):
    """Schema para resposta de resumo"""
    id: int
    user_id: int
    challenge_id: Optional[int]
    study_date: date
    study_time: int
    difficulty: DifficultyEnum
    summary_text: str
    photo_url: Optional[str]
    objectives: List[SummaryObjectiveResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
