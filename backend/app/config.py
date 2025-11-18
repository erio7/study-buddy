from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configurações da aplicação StudyBuddy"""
    
    # Banco de Dados
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/studybuddy_db"
    
    # Segurança
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:5173"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings( )
