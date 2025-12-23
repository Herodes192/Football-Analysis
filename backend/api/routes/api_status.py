"""
API Status and monitoring endpoints
"""
from fastapi import APIRouter
from services.football_api_service import get_football_api_service

router = APIRouter()
football_api = get_football_api_service()


@router.get("/api-usage")
async def get_api_usage():
    """
    Get current API usage statistics
    Shows how many calls have been made today and how many remain
    """
    stats = football_api.get_api_usage_stats()
    
    return {
        "status": "ok",
        "usage": stats,
        "warnings": [
            "⚠️ Limited to 100 API calls per day",
            "💡 Use cached data when possible",
            "🔄 Counter resets daily at midnight"
        ]
    }
