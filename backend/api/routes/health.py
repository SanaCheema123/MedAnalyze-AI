from fastapi import APIRouter
from api.models.schemas import HealthResponse
from config.settings import GEMINI_API_KEY, APP_ENV

router = APIRouter()


@router.get("/")
def root():
    return {"message": "🏥 MedAnalyze AI Backend is running", "docs": "/docs"}


@router.get("/health", response_model=HealthResponse)
def health_check():
    gemini_ok = bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        gemini_connected=gemini_ok,
        environment=APP_ENV,
    )
