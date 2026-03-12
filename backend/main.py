from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import analysis, chat, history, health
from api.middleware.logger import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🏥 MedAnalyze API starting up...")
    yield
    print("🏥 MedAnalyze API shutting down...")


app = FastAPI(
    title="MedAnalyze AI — Backend API",
    description="FastAPI backend for medical report analysis using Google Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(health.router,   tags=["Health"])
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(chat.router,     prefix="/api/v1", tags=["Chat"])
app.include_router(history.router,  prefix="/api/v1", tags=["History"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
