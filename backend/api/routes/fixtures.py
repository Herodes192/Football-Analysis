"""
Fixtures endpoints - Using SofaScore real data scraper
"""
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from services.sofascore_scraper_service import get_sofascore_service
from config.settings import get_settings
from utils.logger import setup_logger

router = APIRouter()
settings = get_settings()
logger = setup_logger(__name__)
sofascore = get_sofascore_service()


@router.get("/fixtures/upcoming")
async def get_upcoming_fixtures(limit: int = 5):
    """Get Gil Vicente's upcoming fixtures from SofaScore"""
    try:
        fixtures = sofascore.get_team_fixtures(team_name="Gil Vicente", limit=limit)
        
        return {
            "team": "Gil Vicente",
            "fixtures": fixtures,
            "count": len(fixtures),
            "source": "SofaScore (Real Data)"
        }
    except Exception as e:
        logger.error(f"Error fetching fixtures: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch fixtures: {str(e)}")


@router.get("/fixtures/results")
async def get_recent_results(limit: int = 5):
    """Get Gil Vicente's recent results from SofaScore"""
    try:
        results = sofascore.get_team_results(team_name="Gil Vicente", limit=limit)
        
        return {
            "team": "Gil Vicente",
            "results": results,
            "count": len(results),
            "source": "SofaScore (Real Data)"
        }
    except Exception as e:
        logger.error(f"Error fetching results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch results: {str(e)}")


@router.get("/fixtures/{fixture_id}")
async def get_fixture_details(fixture_id: int):
    """Get detailed information about a specific fixture"""
    try:
        # For now, return basic info
        # You can enhance this later with more detailed scraping
        return {
            "fixture_id": fixture_id,
            "message": "Detailed fixture info - coming soon",
            "source": "SofaScore"
        }
    except Exception as e:
        logger.error(f"Error fetching fixture details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch fixture details")
