from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any
from enum import Enum


class AnswerOption(str, Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"


class QuestionCreate(BaseModel):
    """Schema para criar uma nova pergunta"""
    challenge_id: int
    text: str
    options: Dict[str, str]  # {"a": "Opção A", "b": "Opção B", ...}
    correct_answer: AnswerOption


class QuestionResponse(BaseModel):
    """Schema para resposta de pergunta"""
    id: int
    challenge_id: int
    text: str
    options: Dict[str, str]
    correct_answer: AnswerOption
    created_at: datetime
    
    class Config:
        from_attributes = True
