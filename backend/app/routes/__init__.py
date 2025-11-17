from .auth import router as auth_router
from .challenges import router as challenges_router
from .summaries import router as summaries_router
from .questions import router as questions_router
from .results import router as results_router
from .dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "challenges_router",
    "summaries_router",
    "questions_router",
    "results_router",
    "dashboard_router",
]
