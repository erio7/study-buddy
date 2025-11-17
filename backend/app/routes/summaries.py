from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models import User, Summary, SummaryObjective
from app.schemas.summary import SummaryCreate, SummaryResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/summaries", tags=["Resumos"])


@router.post("", response_model=SummaryResponse, status_code=status.HTTP_201_CREATED)
async def create_summary(
    summary_data: SummaryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo resumo de estudo.
    
    - **challenge_id**: ID do desafio (opcional)
    - **study_date**: Data do estudo
    - **study_time**: Tempo de estudo em minutos
    - **difficulty**: Nível de dificuldade (Fácil, Médio, Difícil)
    - **summary_text**: Texto do resumo
    - **photo_url**: URL da foto (opcional)
    - **objectives**: Lista de objetivos alcançados (opcional)
    """
    # Verificar se já existe um resumo para este dia
    existing_summary = db.query(Summary).filter(
        Summary.user_id == current_user.id,
        Summary.study_date == summary_data.study_date
    ).first()
    
    if existing_summary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um resumo registrado para este dia"
        )
    
    # Criar novo resumo
    new_summary = Summary(
        user_id=current_user.id,
        challenge_id=summary_data.challenge_id,
        study_date=summary_data.study_date,
        study_time=summary_data.study_time,
        difficulty=summary_data.difficulty,
        summary_text=summary_data.summary_text,
        photo_url=summary_data.photo_url
    )
    
    db.add(new_summary)
    db.flush()  # Para obter o ID do resumo
    
    # Adicionar objetivos se fornecidos
    if summary_data.objectives:
        for objective_text in summary_data.objectives:
            objective = SummaryObjective(
                summary_id=new_summary.id,
                objective_text=objective_text
            )
            db.add(objective)
    
    db.commit()
    db.refresh(new_summary)
    
    return new_summary


@router.get("", response_model=List[SummaryResponse])
async def list_summaries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os resumos do usuário atual"""
    summaries = db.query(Summary).filter(Summary.user_id == current_user.id).all()
    return summaries


@router.get("/{summary_id}", response_model=SummaryResponse)
async def get_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um resumo específico"""
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumo não encontrado"
        )
    
    return summary


@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta um resumo"""
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumo não encontrado"
        )
    
    db.delete(summary)
    db.commit()
