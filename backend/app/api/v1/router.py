from fastapi import APIRouter
from .endpoints import (
    # chains,
    # questions,
    # configurations,
    # answers,
    # comments,
    sessions,
)

api_router = APIRouter()

api_router.include_router(sessions.router)
# api_router.include_router(chains.router, prefix="/chains", tags=["chains"])
# api_router.include_router(
#     questions.router, prefix="/questions", tags=["questions"]
# )
# api_router.include_router(
#     configurations.router, prefix="/configurations", tags=["configurations"]
# )
# api_router.include_router(answers.router, prefix="/answers", tags=["answers"])
# api_router.include_router(
#     comments.router, prefix="/comments", tags=["comments"]
# )
