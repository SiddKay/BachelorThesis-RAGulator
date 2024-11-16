from fastapi import APIRouter
from app.api.v1.endpoints.sessions import router as sessions_router
from app.api.v1.endpoints.chains import router as chains_router

api_router = APIRouter()

api_router.include_router(sessions_router)
api_router.include_router(chains_router)
