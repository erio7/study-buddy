from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Question, Challenge
from app.schemas.question import QuestionCreate, QuestionResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/questions", tags=["Perguntas"])


@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova pergunta para um desafio.
    
    - **challenge_id**: ID do desafio
    - **text**: Texto da pergunta
    - **options**: Opções de resposta (JSON: {"a": "Opção A", "b": "Opção B", ...})
    - **correct_answer**: Resposta correta (a, b, c, d ou e)
    """
    # Verificar se o desafio existe e pertence ao usuário
    challenge = db.query(Challenge).filter(
        Challenge.id == question_data.challenge_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafio não encontrado"
        )
    
    # Criar nova pergunta
    new_question = Question(
        challenge_id=question_data.challenge_id,
        text=question_data.text,
        options=question_data.options,
        correct_answer=question_data.correct_answer.value
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return new_question


@router.get("/challenge/{challenge_id}", response_model=List[QuestionResponse])
async def list_questions_by_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas as perguntas de um desafio específico"""
    # Verificar se o desafio existe e pertence ao usuário
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafio não encontrado"
        )
    
    questions = db.query(Question).filter(Question.challenge_id == challenge_id).all()
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de uma pergunta específica"""
    question = db.query(Question).join(Challenge).filter(
        Question.id == question_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta uma pergunta"""
    question = db.query(Question).join(Challenge).filter(
        Question.id == question_id,
        Challenge.user_id == current_user.id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrado"
        )
    
    db.delete(question)
    db.commit()
