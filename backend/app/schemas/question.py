from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class QuestionCreate(BaseModel):
    """Schema para criar uma nova pergunta"""
    summary_id: int
    text: str
    options: Dict[str, str]  # {"a": "Opção A", "b": "Opção B", ...}
    correct_answer: str  # 'a', 'b', 'c', 'd', 'e'


class QuestionResponse(BaseModel):
    """Schema para resposta de pergunta"""
    id: int
    summary_id: int
    text: str
    options: Dict[str, str]
    correct_answer: str
    created_at: datetime
    
    class Config:
        from_attributes = True
