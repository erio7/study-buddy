from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChallengeCreate(BaseModel):
    """Schema para criar um novo desafio"""
    name: str
    subject: str
    description: Optional[str] = None
    daily_time: int  # Minutos
    duration: int  # Dias
    photo_url: Optional[str] = None


class ChallengeUpdate(BaseModel):
    """Schema para atualizar um desafio"""
    name: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    daily_time: Optional[int] = None
    duration: Optional[int] = None
    photo_url: Optional[str] = None


class ChallengeResponse(BaseModel):
    """Schema para resposta de desafio"""
    id: int
    user_id: int
    name: str
    subject: str
    description: Optional[str]
    daily_time: int
    duration: int
    photo_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
