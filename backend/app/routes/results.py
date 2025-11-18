from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, TestResult, Answer, Question, Summary
from app.schemas.test_result import (
    TestResultResponse,
    SubmitAnswersRequest,
    AnswerResponse
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/results", tags=["Resultados"])


@router.post("/submit", response_model=TestResultResponse, status_code=status.HTTP_201_CREATED)
async def submit_answers(
    request: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submete as respostas de um teste e calcula o resultado.
    
    - **summary_id**: ID do resumo
    - **answers**: Dicionário com as respostas (ex: {"q1": "a", "q2": "b", ...})
    - **time_spent**: Tempo gasto no teste em minutos (opcional)
    """
    # Verificar se o resumo existe e pertence ao usuário
    summary = db.query(Summary).filter(
        Summary.id == request.summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumo não encontrado"
        )
    
    # Obter todas as perguntas do resumo
    questions = db.query(Question).filter(Question.summary_id == request.summary_id).all()
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este resumo não possui perguntas"
        )
    
    # Calcular o resultado
    correct_count = 0
    total_count = len(questions)
    answers_list = []
    
    for question in questions:
        # Obter a resposta do usuário
        question_key = f"q{question.id}"
        user_answer = request.answers.get(question_key)
        
        if user_answer is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resposta faltando para a pergunta {question.id}"
            )
        
        # Verificar se a resposta está correta
        is_correct = user_answer == question.correct_answer
        
        if is_correct:
            correct_count += 1
        
        answers_list.append({
            "question_id": question.id,
            "user_answer": user_answer,
            "is_correct": is_correct
        })
    
    # Calcular a pontuação
    score = int((correct_count / total_count) * 100)
    
    # Criar o resultado do teste
    test_result = TestResult(
        user_id=current_user.id,
        summary_id=request.summary_id,
        score=score,
        correct_count=correct_count,
        total_count=total_count,
        time_spent=request.time_spent
    )
    
    db.add(test_result)
    db.flush()  # Para obter o ID do resultado
    
    # Adicionar as respostas
    for answer_data in answers_list:
        answer = Answer(
            test_result_id=test_result.id,
            question_id=answer_data["question_id"],
            user_answer=answer_data["user_answer"],
            is_correct=answer_data["is_correct"]
        )
        db.add(answer)
    
    db.commit()
    db.refresh(test_result)
    
    return test_result


@router.get("/{result_id}", response_model=TestResultResponse)
async def get_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um resultado de teste específico"""
    result = db.query(TestResult).filter(
        TestResult.id == result_id,
        TestResult.user_id == current_user.id
    ).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado não encontrado"
        )
    
    return result


@router.get("/summary/{summary_id}", response_model=List[TestResultResponse])
async def list_results_by_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os resultados de um resumo específico"""
    # Verificar se o resumo existe
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resumo não encontrado"
        )
    
    results = db.query(TestResult).filter(
        TestResult.summary_id == summary_id,
        TestResult.user_id == current_user.id
    ).all()
    
    return results


@router.get("", response_model=List[TestResultResponse])
async def list_all_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os resultados do usuário atual"""
    results = db.query(TestResult).filter(TestResult.user_id == current_user.id).all()
    return results
