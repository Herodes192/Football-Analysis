"""
Tactical analysis endpoints
"""
from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List

from services.tactical_analysis_service import get_tactical_analysis_service
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)
tactical_service = get_tactical_analysis_service()


@router.post("/tactical/analyze")
async def analyze_opponent_tactics(matches: List[Dict] = Body(...)):
    """
    Analyze opponent tactical patterns based on provided match data
    
    Request body should contain a list of match dictionaries with:
    - formation
    - statistics (possession, shots, etc.)
    - goals_scored, goals_conceded
    - result (W/D/L)
    - is_home (boolean)
    """
    try:
        analysis = tactical_service.analyze_opponent(matches)
        
        return {
            "analysis": analysis,
            "matches_analyzed": len(matches)
        }
    except Exception as e:
        logger.error(f"Error analyzing opponent tactics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze tactics")


@router.post("/tactical/recommendations")
async def get_tactical_recommendations(
    opponent_analysis: Dict = Body(...),
    gil_vicente_formation: str = Body(default="4-3-3")
):
    """
    Generate tactical recommendations for Gil Vicente based on opponent analysis
    
    Request body should contain:
    - opponent_analysis: Result from /tactical/analyze endpoint
    - gil_vicente_formation: Preferred formation (optional, default: 4-3-3)
    """
    try:
        recommendations = tactical_service.generate_recommendations(
            opponent_analysis=opponent_analysis,
            gil_vicente_formation=gil_vicente_formation
        )
        
        return {
            "recommendations": recommendations,
            "opponent_formation": opponent_analysis.get("formations", {}).get("primary_formation")
        }
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


@router.post("/tactical/match-brief")
async def generate_match_brief(
    opponent_team_id: int = Body(...),
    matches: List[Dict] = Body(...),
    gil_vicente_formation: str = Body(default="4-3-3")
):
    """
    Generate complete pre-match tactical brief
    
    Combines analysis and recommendations into a comprehensive brief
    """
    try:
        # Analyze opponent
        analysis = tactical_service.analyze_opponent(matches)
        
        # Generate recommendations
        recommendations = tactical_service.generate_recommendations(
            opponent_analysis=analysis,
            gil_vicente_formation=gil_vicente_formation
        )
        
        brief = {
            "opponent_team_id": opponent_team_id,
            "analysis": analysis,
            "recommendations": recommendations,
            "summary": {
                "opponent_formation": analysis.get("formations", {}).get("primary_formation"),
                "recommended_formation": recommendations.get("recommended_formation"),
                "key_focus": recommendations.get("pressing_strategy", {}).get("description"),
                "main_threats": analysis.get("strengths", []),
                "areas_to_exploit": analysis.get("weaknesses", [])
            }
        }
        
        return brief
        
    except Exception as e:
        logger.error(f"Error generating match brief: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate match brief")
