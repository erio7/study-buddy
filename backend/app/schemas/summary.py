from pydantic import BaseModel, field_validator
from datetime import datetime, date
from typing import Optional, List


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
    difficulty: str
    summary_text: str
    photo_url: Optional[str] = None
    objectives: Optional[List[str]] = None
    
    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v):
        valid_difficulties = ["Fácil", "Médio", "Difícil"]
        if v not in valid_difficulties:
            raise ValueError(f"Dificuldade deve ser uma de: {', '.join(valid_difficulties)}")
        return v


class SummaryResponse(BaseModel):
    """Schema para resposta de resumo"""
    id: int
    user_id: int
    challenge_id: Optional[int]
    study_date: date
    study_time: int
    difficulty: str
    summary_text: str
    photo_url: Optional[str]
    objectives: List[SummaryObjectiveResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
