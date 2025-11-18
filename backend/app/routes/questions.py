from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Question, Summary
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
    Cria uma nova pergunta para um resumo.
    
    - **summary_id**: ID do resumo
    - **text**: Texto da pergunta
    - **options**: Opções de resposta (JSON: {"a": "Opção A", "b": "Opção B", ...})
    - **correct_answer**: Resposta correta (a, b, c, d ou e)
    """
    # Verificar se o resumo existe e pertence ao usuário
    summary = db.query(Summary).filter(
        Summary.id == question_data.summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumo não encontrado"
        )
    
    # Criar nova pergunta
    new_question = Question(
        summary_id=question_data.summary_id,
        text=question_data.text,
        options=question_data.options,
        correct_answer=question_data.correct_answer
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return new_question


@router.get("/summary/{summary_id}", response_model=List[QuestionResponse])
async def list_questions_by_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas as perguntas de um resumo específico"""
    # Verificar se o resumo existe e pertence ao usuário
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumo não encontrado"
        )
    
    questions = db.query(Question).filter(Question.summary_id == summary_id).all()
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de uma pergunta específica"""
    question = db.query(Question).join(Summary).filter(
        Question.id == question_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza uma pergunta existente"""
    question = db.query(Question).join(Summary).filter(
        Question.id == question_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    # Atualizar campos
    question.summary_id = question_data.summary_id
    question.text = question_data.text
    question.options = question_data.options
    question.correct_answer = question_data.correct_answer
    
    db.commit()
    db.refresh(question)
    
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta uma pergunta"""
    question = db.query(Question).join(Summary).filter(
        Question.id == question_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    db.delete(question)
    db.commit()
