from fastapi import APIRouter
from app.api.v1.endpoints.sessions import router as sessions_router
from app.api.v1.endpoints.chains import router as chains_router
from app.api.v1.endpoints.configurations import router as configurations_router
from app.api.v1.endpoints.questions import router as questions_router
from app.api.v1.endpoints.answers import router as answers_router

api_router = APIRouter()

api_router.include_router(sessions_router)
api_router.include_router(chains_router)
api_router.include_router(configurations_router)
api_router.include_router(questions_router)
api_router.include_router(answers_router)
