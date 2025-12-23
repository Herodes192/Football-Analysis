"""
Gil Vicente Tactical Intelligence Platform - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import tactical, health, api_status, match_analysis, real_fixtures, opponent_stats, tactical_plan
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
    logger.info(f"📊 Enhanced opponent statistics available")
    logger.info(f"🧠 AI-powered tactical planning available")
    logger.info(f"🔑 API fallback system active")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="Gil Vicente Tactical Intelligence Platform",
    description="Tactical analysis and opponent intelligence system for Gil Vicente FC",
    version="3.2.0",
    lifespan=lifespan
)

# CORS middleware - MUST be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(api_status.router, prefix="/api/v1", tags=["API Status"])
app.include_router(real_fixtures.router, prefix="/api/v1", tags=["Fixtures"])
app.include_router(opponent_stats.router, prefix="/api/v1", tags=["Opponent Statistics"])
app.include_router(tactical_plan.router, prefix="/api/v1", tags=["Tactical Plan"])
app.include_router(match_analysis.router, prefix="/api/v1", tags=["Match Analysis"])
app.include_router(tactical.router, prefix="/api/v1", tags=["Tactical Analysis"])


@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "name": "Gil Vicente Tactical Intelligence Platform",
        "version": "3.2.0",
        "status": "operational",
        "features": [
            "Real-time fixture tracking",
            "AI-powered match analysis", 
            "Comprehensive opponent statistics",
            "Tactical plan generation with evidence",
            "Form analysis and predictions",
            "Automatic API key fallback"
        ],
        "endpoints": {
            "health": "/api/v1/health",
            "fixtures": "/api/v1/fixtures/all",
            "opponent_stats": "/api/v1/opponent-stats/{opponent_id}",
            "tactical_plan": "/api/v1/tactical-plan/{opponent_id}",
            "match_analysis": "/api/v1/match-analysis/{opponent_id}"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
