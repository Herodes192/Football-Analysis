"""
Match Analysis Service - With automatic API key fallback
"""
import httpx
from typing import Dict, List
from services.advanced_stats_analyzer import get_advanced_stats_analyzer
from services.tactical_ai_engine import get_tactical_ai_engine
from utils.logger import setup_logger
from utils.api_client import get_api_client

logger = setup_logger(__name__)


class MatchAnalysisService:
    def __init__(self):
        self.stats_analyzer = get_advanced_stats_analyzer()
        self.ai_engine = get_tactical_ai_engine()
        self.api_client = get_api_client()
    
    async def analyze_match(self, opponent_id: str, opponent_name: str) -> Dict:
        """Generate comprehensive match analysis with automatic API key fallback"""
        try:
            # Get all league matches with automatic fallback
            data = await self.api_client.get(
                "/football-get-all-matches-by-league",
                params={"leagueid": 61}
            )
            
            matches = data.get('response', {}).get('matches', [])
            
            # Get Gil Vicente form
            gil_form = await self._get_team_recent_form(matches, "9764", "Gil Vicente")
            
            # Get opponent form
            opp_form = await self._get_team_recent_form(matches, opponent_id, opponent_name)
            
            # Advanced stats analysis
            opponent_advanced_stats = {}
            if opp_form['recent_matches']:
                opponent_advanced_stats = self.stats_analyzer.analyze_last_game(
                    opp_form['recent_matches'], 
                    opponent_name
                )
            
            # Tactical recommendations
            ai_recommendations = self.ai_engine.generate_recommendations(
                opponent_advanced_stats,
                None  # We could pass Gil Vicente stats here too
            )
            
            return {
                "match": f"Gil Vicente vs {opponent_name}",
                "gil_vicente_form": gil_form,
                "opponent_form": opp_form,
                "defensive_vulnerabilities": self._analyze_defensive_vulnerabilities(opp_form),
                "gil_attacking_analysis": self._analyze_gil_attacking(gil_form),
                "tactical_game_plan": self._generate_game_plan(gil_form, opp_form),
                "opponent_advanced_stats": opponent_advanced_stats,
                "ai_recommendations": ai_recommendations,
                "generated_at": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
    
    async def _get_team_recent_form(self, all_matches: List[Dict], team_id: str, team_name: str) -> Dict:
        """Get team's recent form from matches list"""
        team_matches = []
        
        for match in all_matches:
            home_id = str(match.get('home', {}).get('id', ''))
            away_id = str(match.get('away', {}).get('id', ''))
            
            if team_id in [home_id, away_id] and match.get('status', {}).get('finished'):
                team_matches.append(match)
        
        # Sort by date (most recent first) and take last 5
        team_matches.sort(key=lambda x: x.get('status', {}).get('utcTime', ''), reverse=True)
        recent_matches = team_matches[:5]
        
        # Calculate form
        form = self._calculate_form(recent_matches, team_id)
        
        return {
            "team_name": team_name,
            "recent_matches": recent_matches,
            "form_summary": form
        }
    
    def _calculate_form(self, matches: List[Dict], team_id: str) -> Dict:
        """Calculate team form from recent matches"""
        wins = draws = losses = 0
        goals_scored = goals_conceded = 0
        
        for match in matches:
            is_home = str(match['home']['id']) == str(team_id)
            team_score = match['home']['score'] if is_home else match['away']['score']
            opp_score = match['away']['score'] if is_home else match['home']['score']
            
            goals_scored += team_score
            goals_conceded += opp_score
            
            if team_score > opp_score:
                wins += 1
            elif team_score < opp_score:
                losses += 1
            else:
                draws += 1
        
        total_games = len(matches)
        
        return {
            "form_string": f"{wins}W-{draws}D-{losses}L",
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_scored": goals_scored,
            "goals_conceded": goals_conceded,
            "goal_difference": goals_scored - goals_conceded,
            "points": wins * 3 + draws,
            "games_played": total_games,
            "avg_goals_scored": round(goals_scored / total_games, 2) if total_games > 0 else 0,
            "avg_goals_conceded": round(goals_conceded / total_games, 2) if total_games > 0 else 0
        }
    
    def _analyze_defensive_vulnerabilities(self, opponent_form: Dict) -> Dict:
        """Analyze opponent's defensive weaknesses"""
        form = opponent_form.get('form_summary', {})
        
        return {
            "conceding_rate": form.get('avg_goals_conceded', 0),
            "clean_sheets": sum(1 for m in opponent_form['recent_matches'] 
                               if self._team_kept_clean_sheet(m, opponent_form['team_name'])),
            "vulnerability_rating": "High" if form.get('avg_goals_conceded', 0) > 1.5 else "Medium" if form.get('avg_goals_conceded', 0) > 1 else "Low"
        }
    
    def _team_kept_clean_sheet(self, match: Dict, team_name: str) -> bool:
        """Check if team kept a clean sheet"""
        is_home = match['home']['name'] == team_name
        goals_conceded = match['away']['score'] if is_home else match['home']['score']
        return goals_conceded == 0
    
    def _analyze_gil_attacking(self, gil_form: Dict) -> Dict:
        """Analyze Gil Vicente's attacking performance"""
        form = gil_form.get('form_summary', {})
        
        return {
            "scoring_rate": form.get('avg_goals_scored', 0),
            "recent_form": form.get('form_string', ''),
            "attack_rating": "Strong" if form.get('avg_goals_scored', 0) >= 1.5 else "Average" if form.get('avg_goals_scored', 0) >= 1 else "Weak"
        }
    
    def _generate_game_plan(self, gil_form: Dict, opp_form: Dict) -> Dict:
        """Generate tactical game plan"""
        gil_attack = gil_form['form_summary'].get('avg_goals_scored', 0)
        opp_defense = opp_form['form_summary'].get('avg_goals_conceded', 0)
        
        if opp_defense > 1.5:
            approach = "Aggressive - Opponent is defensively weak"
            formation = "4-3-3 or 4-2-4"
        elif gil_attack >= 1.5:
            approach = "Balanced - Capitalize on good form"
            formation = "4-2-3-1"
        else:
            approach = "Cautious - Build confidence"
            formation = "4-4-2 or 4-5-1"
        
        return {
            "recommended_approach": approach,
            "suggested_formation": formation,
            "key_focus": "Exploit defensive vulnerabilities" if opp_defense > 1.5 else "Maintain defensive solidity"
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# Singleton instance
_service = None

def get_match_analysis_service() -> MatchAnalysisService:
    """Get singleton match analysis service instance"""
    global _service
    if _service is None:
        _service = MatchAnalysisService()
    return _service
