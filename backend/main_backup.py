"""
Gil Vicente Tactical Intelligence Platform - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import tactical, health, api_status, match_analysis, real_fixtures
from config.settings import get_settings
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Gil Vicente Tactical Intelligence Platform...")
    logger.info(f"🎯 Real-time match analysis enabled")
    logger.info(f"⚽ Using Free API Live Football Data")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="Gil Vicente Tactical Intelligence Platform",
    description="Tactical analysis and opponent intelligence system for Gil Vicente FC",
    version="3.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(api_status.router, prefix="/api/v1", tags=["API Status"])
app.include_router(real_fixtures.router, prefix="/api/v1", tags=["Fixtures"])
app.include_router(match_analysis.router, prefix="/api/v1", tags=["Match Analysis"])
app.include_router(tactical.router, prefix="/api/v1", tags=["Tactical Analysis"])


@app.get("/")
async def root():
    return {
        "message": "Gil Vicente Tactical Intelligence Platform API",
        "version": "3.0.0",
        "docs": "/docs",
        "features": ["Real-time match analysis", "Tactical intelligence", "Form tracking"]
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
