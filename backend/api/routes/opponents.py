"""
Opponents analysis endpoints - Using SofaScore real data
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from services.sofascore_scraper_service import get_sofascore_service
from config.settings import get_settings
from utils.logger import setup_logger

router = APIRouter()
settings = get_settings()
logger = setup_logger(__name__)
sofascore = get_sofascore_service()


@router.get("/opponents")
async def get_opponents_list():
    """Get list of opponents from Primeira Liga"""
    try:
        teams = sofascore.get_league_teams()
        
        # Filter out Gil Vicente
        opponents = [t for t in teams if t['name'] != 'Gil Vicente']
        
        return {
            "season": 2024,
            "opponents": opponents,
            "count": len(opponents),
            "source": "SofaScore (Real Data)"
        }
    except Exception as e:
        logger.error(f"Error fetching opponents list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch opponents: {str(e)}")


@router.get("/opponents/{team_id}/matches")
async def get_opponent_matches(team_id: int, limit: int = 10):
    """Get opponent's recent match history"""
    try:
        # Get team name from ID (simplified - you can add a mapping)
        return {
            "team_id": team_id,
            "message": "Opponent match history - coming soon",
            "note": "Use /opponents/{team_name}/recent for real data"
        }
    except Exception as e:
        logger.error(f"Error fetching opponent matches: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch opponent matches")


@router.get("/opponents/{team_name}/recent")
async def get_opponent_recent_by_name(team_name: str, limit: int = 5):
    """Get opponent's recent form by team name"""
    try:
        results = sofascore.get_team_results(team_name=team_name, limit=limit)
        
        return {
            "team_name": team_name,
            "recent_matches": results,
            "count": len(results),
            "source": "SofaScore (Real Data)"
        }
    except Exception as e:
        logger.error(f"Error fetching opponent recent form: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch opponent data: {str(e)}")


@router.get("/opponents/{team_id}/tactical")
async def get_opponent_tactical_info(team_id: int):
    """Get opponent's tactical information"""
    try:
        return {
            "team_id": team_id,
            "message": "Tactical analysis - coming soon",
            "note": "Enhanced tactical data will be added"
        }
    except Exception as e:
        logger.error(f"Error fetching opponent tactical info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch opponent tactical information")
