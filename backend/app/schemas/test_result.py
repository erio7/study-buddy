from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum


class AnswerOption(str, Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"


class AnswerCreate(BaseModel):
    """Schema para criar uma resposta"""
    question_id: int
    user_answer: AnswerOption


class AnswerResponse(BaseModel):
    """Schema para resposta de resposta"""
    id: int
    test_result_id: int
    question_id: int
    user_answer: AnswerOption
    is_correct: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TestResultCreate(BaseModel):
    """Schema para criar um resultado de teste"""
    challenge_id: int
    score: int
    correct_count: int
    total_count: int
    time_spent: Optional[int] = None


class TestResultResponse(BaseModel):
    """Schema para resposta de resultado de teste"""
    id: int
    user_id: int
    challenge_id: int
    score: int
    correct_count: int
    total_count: int
    time_spent: Optional[int]
    answers: List[AnswerResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SubmitAnswersRequest(BaseModel):
    """Schema para submeter respostas de um teste"""
    challenge_id: int
    answers: Dict[str, AnswerOption]  # {"q1": "a", "q2": "b", ...}
    time_spent: Optional[int] = None
