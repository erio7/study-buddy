from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import (
    auth_router,
    challenges_router,
    summaries_router,
    questions_router,
    results_router,
    dashboard_router
)

# Criar aplicação FastAPI
app = FastAPI(
    title="StudyBuddy API",
    description="API para o gerenciador de estudos StudyBuddy",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth_router)
app.include_router(challenges_router)
app.include_router(summaries_router)
app.include_router(questions_router)
app.include_router(results_router)
app.include_router(dashboard_router)


@app.get("/", tags=["Root"])
async def root():
    """Rota raiz da API"""
    return {
        "message": "Bem-vindo à StudyBuddy API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Verifica a saúde da API"""
    return {
        "status": "healthy",
        "service": "StudyBuddy API"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
