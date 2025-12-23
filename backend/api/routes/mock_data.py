"""
Mock data endpoints for development/testing
Returns realistic Gil Vicente data structure without API calls
"""
from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import List, Dict

router = APIRouter()

# Sample opponents from 2024 season
OPPONENTS = [
    {"id": 211, "name": "Benfica", "logo": "https://media.api-sports.io/football/teams/211.png"},
    {"id": 212, "name": "Porto", "logo": "https://media.api-sports.io/football/teams/212.png"},
    {"id": 228, "name": "Gil Vicente", "logo": "https://media.api-sports.io/football/teams/228.png"},
    {"id": 210, "name": "Sporting CP", "logo": "https://media.api-sports.io/football/teams/210.png"},
    {"id": 218, "name": "Braga", "logo": "https://media.api-sports.io/football/teams/218.png"},
    {"id": 236, "name": "Vitória Guimarães", "logo": "https://media.api-sports.io/football/teams/236.png"},
    {"id": 234, "name": "Moreirense", "logo": "https://media.api-sports.io/football/teams/234.png"},
    {"id": 215, "name": "Famalicão", "logo": "https://media.api-sports.io/football/teams/215.png"},
    {"id": 233, "name": "Santa Clara", "logo": "https://media.api-sports.io/football/teams/233.png"},
    {"id": 230, "name": "Estoril", "logo": "https://media.api-sports.io/football/teams/230.png"},
]


def create_fixture(opponent_id: int, opponent_name: str, days_from_now: int, is_home: bool):
    """Create a realistic fixture structure"""
    match_date = datetime.now() + timedelta(days=days_from_now)
    
    home_team = {"id": 228, "name": "Gil Vicente"} if is_home else {"id": opponent_id, "name": opponent_name}
    away_team = {"id": opponent_id, "name": opponent_name} if is_home else {"id": 228, "name": "Gil Vicente"}
    
    return {
        "fixture": {
            "id": 10000 + opponent_id + days_from_now,
            "date": match_date.isoformat(),
            "timestamp": int(match_date.timestamp()),
            "venue": {"name": "Estádio Cidade de Barcelos" if is_home else f"Stadium {opponent_name}"},
            "status": {"short": "NS", "long": "Not Started"}
        },
        "league": {
            "id": 94,
            "name": "Primeira Liga",
            "country": "Portugal",
            "logo": "https://media.api-sports.io/football/leagues/94.png",
            "season": 2025
        },
        "teams": {
            "home": home_team,
            "away": away_team
        },
        "goals": {"home": None, "away": None}
    }


@router.get("/fixtures/upcoming")
async def get_upcoming_fixtures(limit: int = 5):
    """Get Gil Vicente's upcoming fixtures with 2025 dates"""
    fixtures = [
        create_fixture(211, "Benfica", 7, False),        # Away in 7 days (28 Dec)
        create_fixture(212, "Porto", 14, True),          # Home in 14 days 
        create_fixture(236, "Vitória Guimarães", 21, False),  # Away in 21 days
        create_fixture(218, "Braga", 28, True),          # Home in 28 days
        create_fixture(234, "Moreirense", 35, False),    # Away in 35 days
    ]
    
    return {
        "team": "Gil Vicente",
        "fixtures": fixtures[:limit],
        "count": len(fixtures[:limit])
    }


@router.get("/opponents")
async def get_opponents():
    """Get list of opponents"""
    return {
        "season": 2025,
        "opponents": OPPONENTS,
        "count": len(OPPONENTS)
    }


@router.get("/opponents/{team_id}/recent")
async def get_opponent_recent_form(team_id: int):
    """Get opponent's recent form (using 2024 data structure, 2025 dates)"""
    opponent = next((o for o in OPPONENTS if o["id"] == team_id), None)
    if not opponent:
        return {"error": "Opponent not found"}
    
    # Sample recent matches
    recent_matches = [
        {
            "date": (datetime.now() - timedelta(days=7)).isoformat(),
            "home_team": opponent["name"],
            "away_team": "Porto",
            "score": "2-1",
            "result": "W"
        },
        {
            "date": (datetime.now() - timedelta(days=14)).isoformat(),
            "home_team": "Sporting CP",
            "away_team": opponent["name"],
            "score": "3-0",
            "result": "L"
        },
        {
            "date": (datetime.now() - timedelta(days=21)).isoformat(),
            "home_team": opponent["name"],
            "away_team": "Braga",
            "score": "1-1",
            "result": "D"
        },
    ]
    
    return {
        "team": opponent,
        "form": "WLD",
        "recent_matches": recent_matches,
        "statistics": {
            "goals_scored": 12,
            "goals_conceded": 8,
            "wins": 5,
            "draws": 3,
            "losses": 2,
            "form_percentage": 65
        }
    }


@router.get("/opponents/{team_id}/tactical")
async def get_opponent_tactical_profile(team_id: int):
    """Get opponent's tactical analysis"""
    opponent = next((o for o in OPPONENTS if o["id"] == team_id), None)
    if not opponent:
        return {"error": "Opponent not found"}
    
    return {
        "team": opponent,
        "formation": "4-3-3",
        "playing_style": "Possession-based",
        "strengths": [
            "Strong midfield control",
            "Quick counter-attacks",
            "Set-piece efficiency"
        ],
        "weaknesses": [
            "Vulnerable to pressing",
            "Defensive transitions",
            "Lack of aerial presence"
        ],
        "key_players": [
            {"name": "Player A", "position": "Midfielder", "rating": 7.5},
            {"name": "Player B", "position": "Forward", "rating": 7.2}
        ],
        "recommendations": [
            "Press high to disrupt build-up play",
            "Exploit spaces behind full-backs",
            "Target aerial duels in defensive third"
        ]
    }
