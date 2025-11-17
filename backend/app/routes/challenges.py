from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate, ChallengeResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/challenges", tags=["Desafios"])


@router.post("", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge_data: ChallengeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo desafio de estudo.
    
    - **name**: Nome do desafio
    - **subject**: Disciplina/Assunto
    - **description**: Descrição (opcional)
    - **daily_time**: Tempo diário em minutos
    - **duration**: Duração em dias
    - **photo_url**: URL da foto (opcional)
    """
    new_challenge = Challenge(
        user_id=current_user.id,
        name=challenge_data.name,
        subject=challenge_data.subject,
        description=challenge_data.description,
        daily_time=challenge_data.daily_time,
        duration=challenge_data.duration,
        photo_url=challenge_data.photo_url
    )
    
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    
    return new_challenge


@router.get("", response_model=List[ChallengeResponse])
async def list_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os desafios do usuário atual"""
    challenges = db.query(Challenge).filter(Challenge.user_id == current_user.id).all()
    return challenges


@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um desafio específico"""
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafio não encontrado"
        )
    
    return challenge


@router.put("/{challenge_id}", response_model=ChallengeResponse)
async def update_challenge(
    challenge_id: int,
    challenge_data: ChallengeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza um desafio existente"""
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafio não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = challenge_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(challenge, field, value)
    
    db.commit()
    db.refresh(challenge)
    
    return challenge


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta um desafio"""
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafio não encontrado"
        )
    
    db.delete(challenge)
    db.commit()
