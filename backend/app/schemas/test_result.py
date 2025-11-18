from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional, List


class AnswerResponse(BaseModel):
    """Schema para resposta de resposta"""
    id: int
    test_result_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TestResultCreate(BaseModel):
    """Schema para criar um resultado de teste"""
    summary_id: int
    score: int
    correct_count: int
    total_count: int
    time_spent: Optional[int] = None


class TestResultResponse(BaseModel):
    """Schema para resposta de resultado de teste"""
    id: int
    user_id: int
    summary_id: int
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
    summary_id: int
    answers: Dict[str, str]  # {"q1": "a", "q2": "b", ...}
    time_spent: Optional[int] = None
