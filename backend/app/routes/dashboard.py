from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from app.database import get_db
from app.models import User, Summary, Challenge, TestResult
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["Dashboard"])


@router.get("/streak-days", response_model=Dict[str, List[str]])
async def get_streak_days(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém as datas de estudo do usuário (para o calendário de streak).
    
    Retorna um dicionário com a chave 'dates' contendo uma lista de datas em formato ISO (YYYY-MM-DD).
    """
    # Obter todos os resumos do usuário
    summaries = db.query(Summary.study_date).filter(
        Summary.user_id == current_user.id
    ).distinct().all()
    
    # Converter para formato ISO
    dates = [summary.study_date.isoformat() for summary in summaries]
    
    return {"dates": dates}


@router.get("/day/{date_str}", response_model=Dict[str, Any])
async def get_day_data(
    date_str: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém os dados de um dia específico.
    
    - **date_str**: Data em formato ISO (YYYY-MM-DD)
    
    Retorna informações sobre o estudo do dia, incluindo tempo gasto, assunto, dificuldade, etc.
    """
    try:
        study_date = datetime.fromisoformat(date_str).date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de data inválido. Use YYYY-MM-DD"
        )
    
    # Obter o resumo do dia
    summary = db.query(Summary).filter(
        Summary.user_id == current_user.id,
        Summary.study_date == study_date
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum registro de estudo para este dia"
        )
    
    # Obter informações do desafio associado (se houver)
    challenge_info = None
    if summary.challenge_id:
        challenge = db.query(Challenge).filter(Challenge.id == summary.challenge_id).first()
        if challenge:
            challenge_info = {
                "id": challenge.id,
                "name": challenge.name,
                "subject": challenge.subject
            }
    
    return {
        "date": study_date.isoformat(),
        "formattedDate": study_date.strftime("%d de %B, %Y"),
        "studyTime": f"{summary.study_time // 60}h {summary.study_time % 60}m",
        "subject": challenge_info["subject"] if challenge_info else "Estudo Geral",
        "difficulty": summary.difficulty.value,
        "summary": summary.summary_text,
        "photo": summary.photo_url,
        "objectives": [obj.objective_text for obj in summary.objectives],
        "completed": True
    }


@router.get("/dashboard/overview", response_model=Dict[str, Any])
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém uma visão geral do dashboard do usuário.
    
    Retorna informações como:
    - Desafios ativos
    - Progresso semanal
    - Metas do mês
    - Últimos resumos
    """
    # Obter desafios ativos
    challenges = db.query(Challenge).filter(Challenge.user_id == current_user.id).all()
    
    # Obter resumos da última semana
    seven_days_ago = date.today() - timedelta(days=7)
    weekly_summaries = db.query(Summary).filter(
        Summary.user_id == current_user.id,
        Summary.study_date >= seven_days_ago
    ).all()
    
    # Calcular tempo total de estudo da semana
    total_study_time = sum(s.study_time for s in weekly_summaries)
    
    # Obter últimos 5 resumos
    recent_summaries = db.query(Summary).filter(
        Summary.user_id == current_user.id
    ).order_by(Summary.study_date.desc()).limit(5).all()
    
    # Obter resultados de testes
    test_results = db.query(TestResult).filter(
        TestResult.user_id == current_user.id
    ).order_by(TestResult.created_at.desc()).limit(5).all()
    
    return {
        "activeChallenges": len(challenges),
        "weeklyStudyTime": f"{total_study_time // 60}h {total_study_time % 60}m",
        "totalStudyDays": len(weekly_summaries),
        "challenges": [
            {
                "id": c.id,
                "name": c.name,
                "subject": c.subject,
                "dailyTime": c.daily_time,
                "duration": c.duration
            }
            for c in challenges
        ],
        "recentSummaries": [
            {
                "id": s.id,
                "date": s.study_date.isoformat(),
                "studyTime": s.study_time,
                "difficulty": s.difficulty.value,
                "summary": s.summary_text[:100] + "..." if len(s.summary_text) > 100 else s.summary_text
            }
            for s in recent_summaries
        ],
        "recentResults": [
            {
                "id": r.id,
                "challengeId": r.challenge_id,
                "score": r.score,
                "correctCount": r.correct_count,
                "totalCount": r.total_count,
                "date": r.created_at.isoformat()
            }
            for r in test_results
        ]
    }
