from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema para criar um novo usuário"""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema para login de usuário"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema para resposta de token"""
    access_token: str
    token_type: str
    user: UserResponse
