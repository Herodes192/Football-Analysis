"""
Match Analysis Service - Deep Tactical Intelligence for Coaching
Integrates Advanced Stats Analyzer and AI Tactical Engine
"""
import httpx
from typing import Dict, List, Optional
from datetime import datetime
from utils.logger import setup_logger
from config.settings import get_settings
from services.advanced_stats_analyzer import get_advanced_stats_analyzer
from services.tactical_ai_engine import get_tactical_ai_engine

settings = get_settings()
logger = setup_logger(__name__)


class MatchAnalysisService:
    """Generate deep tactical analysis for coaching decisions"""
    
    def __init__(self):
        self.api_key = settings.FOOTBALL_API_KEY
        self.base_url = "https://free-api-live-football-data.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }
        # Initialize AI services
        self.stats_analyzer = get_advanced_stats_analyzer()
        self.ai_engine = get_tactical_ai_engine()
    
    async def _get_team_recent_form(self, team_id: str, team_name: str, league_id: int = 61) -> Dict:
        """Get team's recent form and detailed match data"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/football-get-all-matches-by-league",
                    headers=self.headers,
                    params={"leagueid": league_id}
                )
                response.raise_for_status()
                data = response.json()
                
                matches = data.get('response', {}).get('matches', [])
                team_matches = [
                    m for m in matches 
                    if team_id in [str(m.get('home', {}).get('id', '')), str(m.get('away', {}).get('id', ''))]
                ]
                recent = [m for m in team_matches if m.get('status', {}).get('finished', False)][-5:]
                
                wins = draws = losses = 0
                goals_scored = goals_conceded = 0
                first_half_goals_conceded = 0
                second_half_goals_conceded = 0
                clean_sheets = 0
                goals_in_final_15min = 0
                
                for match in recent:
                    is_home = match['home']['id'] == int(team_id)
                    team_score = match['home']['score'] if is_home else match['away']['score']
                    opp_score = match['away']['score'] if is_home else match['home']['score']
                    
                    goals_scored += team_score
                    goals_conceded += opp_score
                    
                    if opp_score == 0:
                        clean_sheets += 1
                    
                    # Estimate time-based patterns
                    if opp_score >= 2:
                        first_half_goals_conceded += 1
                        second_half_goals_conceded += 1
                    elif opp_score == 1:
                        first_half_goals_conceded += 0.5
                        second_half_goals_conceded += 0.5
                    
                    # Teams that concede heavily likely concede late
                    if opp_score >= 3:
                        goals_in_final_15min += 1
                    
                    if team_score > opp_score:
                        wins += 1
                    elif team_score == opp_score:
                        draws += 1
                    else:
                        losses += 1
                
                avg_goals_conceded = goals_conceded / len(recent) if recent else 0
                
                return {
                    "team_name": team_name,
                    "recent_matches": recent,
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "goals_scored": goals_scored,
                    "goals_conceded": goals_conceded,
                    "clean_sheets": clean_sheets,
                    "avg_goals_conceded": round(avg_goals_conceded, 2),
                    "first_half_vulnerability": first_half_goals_conceded,
                    "second_half_vulnerability": second_half_goals_conceded,
                    "late_game_collapses": goals_in_final_15min,
                    "form_string": f"{wins}W-{draws}D-{losses}L"
                }
        except Exception as e:
            logger.error(f"Error fetching form for {team_name}: {e}")
            return {"team_name": team_name, "error": str(e)}
    
    def _analyze_defensive_vulnerabilities(self, opponent_form: Dict) -> Dict:
        """Analyze opponent's defensive weak points"""
        goals_conceded = opponent_form.get('goals_conceded', 0)
        avg_conceded = opponent_form.get('avg_goals_conceded', 0)
        clean_sheets = opponent_form.get('clean_sheets', 0)
        losses = opponent_form.get('losses', 0)
        first_half_vuln = opponent_form.get('first_half_vulnerability', 0)
        second_half_vuln = opponent_form.get('second_half_vulnerability', 0)
        late_collapses = opponent_form.get('late_game_collapses', 0)
        
        vulnerabilities = []
        
        # Overall defensive quality
        if avg_conceded >= 2.5:
            vulnerabilities.append({
                "zone": "Overall Defense",
                "severity": "CRITICAL",
                "detail": f"Conceding {avg_conceded} goals/game - extremely vulnerable",
                "coaching_tip": "Press high and exploit disorganized backline"
            })
        elif avg_conceded >= 1.5:
            vulnerabilities.append({
                "zone": "Overall Defense",
                "severity": "HIGH",
                "detail": f"Conceding {avg_conceded} goals/game - weak defensive structure",
                "coaching_tip": "Target with direct attacks and quick transitions"
            })
        
        # Clean sheet analysis
        if clean_sheets == 0:
            vulnerabilities.append({
                "zone": "Defensive Organization",
                "severity": "CRITICAL",
                "detail": "NO clean sheets in last 5 games - always concede",
                "coaching_tip": "Maintain attacking intent - they WILL give up chances"
            })
        
        # Time-based vulnerabilities
        if second_half_vuln > first_half_vuln * 1.3:
            vulnerabilities.append({
                "zone": "Second Half / Fitness",
                "severity": "HIGH",
                "detail": "Defensive collapse after 45min - fitness issues evident",
                "coaching_tip": "Conserve energy first half, press hard 60min onwards"
            })
        elif first_half_vuln > second_half_vuln * 1.3:
            vulnerabilities.append({
                "zone": "First Half / Concentration",
                "severity": "MEDIUM",
                "detail": "Slow starts - vulnerable in opening phase",
                "coaching_tip": "Start aggressively, score early to break morale"
            })
        
        # Late game collapses
        if late_collapses >= 2:
            vulnerabilities.append({
                "zone": "Final 15 Minutes",
                "severity": "CRITICAL",
                "detail": "Defensive collapses late in games - mental weakness",
                "coaching_tip": "If level at 75min, push for winner - they'll crack"
            })
        
        # Spatial vulnerabilities (inferred from heavy defeats)
        if losses >= 3:
            vulnerabilities.append({
                "zone": "Wide Areas / Flanks",
                "severity": "HIGH",
                "detail": "Multiple heavy defeats suggest wide defensive issues",
                "coaching_tip": "Overload flanks with wingers and fullbacks"
            })
        
        return {
            "vulnerabilities": vulnerabilities,
            "overall_rating": "POOR" if avg_conceded >= 2.0 else "AVERAGE" if avg_conceded >= 1.2 else "SOLID"
        }
    
    def _analyze_attacking_patterns(self, team_form: Dict) -> Dict:
        """Analyze team's attacking capabilities"""
        goals_scored = team_form.get('goals_scored', 0)
        matches = len(team_form.get('recent_matches', []))
        avg_scored = goals_scored / matches if matches else 0
        wins = team_form.get('wins', 0)
        
        patterns = []
        
        if avg_scored < 0.8:
            patterns.append({
                "pattern": "Low Scoring Output",
                "detail": f"Only {goals_scored} goals in {matches} games",
                "recommendation": "Focus on defensive solidity, counter-attack opportunities"
            })
        elif avg_scored >= 1.5:
            patterns.append({
                "pattern": "Strong Attacking Form",
                "detail": f"{goals_scored} goals in {matches} games - good offensive rhythm",
                "recommendation": "Be confident in attack, create chances through possession"
            })
        
        if wins == 0 and avg_scored >= 1.0:
            patterns.append({
                "pattern": "Unlucky in Front of Goal",
                "detail": "Creating but not converting - need clinical finishing",
                "recommendation": "Work on finishing drills, focus on high-quality chances"
            })
        
        return {
            "patterns": patterns,
            "avg_goals": round(avg_scored, 2)
        }
    
    def _generate_tactical_game_plan(self, gil_form: Dict, opponent_form: Dict, 
                                     opponent_name: str, defensive_analysis: Dict) -> Dict:
        """Generate comprehensive tactical game plan for coaching staff"""
        
        game_plan = {
            "formation_recommendation": "",
            "key_tactical_points": [],
            "player_instructions": [],
            "game_phases": {
                "first_15min": "",
                "minutes_15_45": "",
                "half_time_adjustments": "",
                "minutes_45_75": "",
                "final_15min": ""
            },
            "set_piece_strategy": ""
        }
        
        # Formation based on opponent weakness
        opp_avg_conceded = opponent_form.get('avg_goals_conceded', 0)
        if opp_avg_conceded >= 2.0:
            game_plan["formation_recommendation"] = "4-3-3 (Attacking) - Exploit weak defense with width and pace"
        elif opp_avg_conceded >= 1.5:
            game_plan["formation_recommendation"] = "4-2-3-1 - Balance attack with two holding midfielders"
        else:
            game_plan["formation_recommendation"] = "4-5-1 - Compact defensive shape, counter-attack"
        
        # Key tactical points
        for vuln in defensive_analysis['vulnerabilities']:
            if vuln['severity'] in ['CRITICAL', 'HIGH']:
                game_plan["key_tactical_points"].append(f"TARGET: {vuln['zone']} - {vuln['coaching_tip']}")
        
        # Player instructions
        if opponent_form.get('late_game_collapses', 0) >= 2:
            game_plan["player_instructions"].append("Forwards: Stay high, energy conservation until 70min mark")
            game_plan["player_instructions"].append("Midfield: Control tempo, don't over-commit early")
        
        if opponent_form.get('clean_sheets', 0) == 0:
            game_plan["player_instructions"].append("Wingers: Attack with confidence - they ALWAYS concede")
            game_plan["player_instructions"].append("Fullbacks: Push forward in wide areas")
        
        # Game phases
        second_half_weak = opponent_form.get('second_half_vulnerability', 0) > opponent_form.get('first_half_vulnerability', 0)
        
        if second_half_weak:
            game_plan["game_phases"]["first_15min"] = "Stay compact, feel out opponent, don't over-commit"
            game_plan["game_phases"]["minutes_15_45"] = "Gradual pressure increase, test defensive flanks"
            game_plan["game_phases"]["half_time_adjustments"] = "Prepare for second-half push, fresh legs ready"
            game_plan["game_phases"]["minutes_45_75"] = "AGGRESSIVE - Opponent fatigues, press high, overload attacks"
            game_plan["game_phases"]["final_15min"] = "CRITICAL PHASE - They collapse late, push for goals"
        else:
            game_plan["game_phases"]["first_15min"] = "START STRONG - Score early to damage morale"
            game_plan["game_phases"]["minutes_15_45"] = "Maintain intensity, don't allow comeback"
            game_plan["game_phases"]["half_time_adjustments"] = "Assess lead, prepare for opponent changes"
            game_plan["game_phases"]["minutes_45_75"] = "Control tempo, manage energy"
            game_plan["game_phases"]["final_15min"] = "Stay solid, close out game professionally"
        
        # Set pieces
        if opp_avg_conceded >= 2.0:
            game_plan["set_piece_strategy"] = "CRITICAL WEAPON - Opponent weak on set pieces. Target tall players for headers, practice corner routines"
        else:
            game_plan["set_piece_strategy"] = "Standard set-piece approach, focus on delivery quality"
        
        return game_plan
    
    async def analyze_match(self, opponent_id: str, opponent_name: str) -> Dict:
        """Generate comprehensive coaching-focused match analysis with AI"""
        logger.info(f"Generating tactical analysis: Gil Vicente vs {opponent_name}")
        
        # Get form for both teams
        gil_form = await self._get_team_recent_form("9764", "Gil Vicente")
        opp_form = await self._get_team_recent_form(opponent_id, opponent_name)
        
        # Deep tactical analysis
        defensive_analysis = self._analyze_defensive_vulnerabilities(opp_form)
        attacking_analysis = self._analyze_attacking_patterns(gil_form)
        game_plan = self._generate_tactical_game_plan(gil_form, opp_form, opponent_name, defensive_analysis)
        
        # Advanced stats analysis for opponent's last game
        opponent_advanced_stats = None
        if opp_form.get('recent_matches'):
            try:
                opponent_advanced_stats = self.stats_analyzer.analyze_last_game(
                    opp_form['recent_matches'],
                    opponent_name
                )
                logger.info(f"✅ Advanced stats generated for {opponent_name}")
            except Exception as e:
                logger.error(f"❌ Error analyzing advanced stats: {e}")
        
        # AI tactical recommendations
        ai_recommendations = None
        if opponent_advanced_stats:
            try:
                ai_recommendations = self.ai_engine.generate_recommendations(
                    opponent_advanced_stats,
                    None  # Gil stats can be added later for more advanced AI
                )
                confidence = ai_recommendations.get('ai_confidence', {}).get('score', 0)
                logger.info(f"🤖 AI recommendations generated with {confidence}% confidence")
            except Exception as e:
                logger.error(f"❌ Error generating AI recommendations: {e}")
        
        return {
            "match": f"Gil Vicente vs {opponent_name}",
            "gil_vicente_form": gil_form,
            "opponent_form": opp_form,
            "defensive_vulnerabilities": defensive_analysis,
            "gil_attacking_analysis": attacking_analysis,
            "tactical_game_plan": game_plan,
            "opponent_advanced_stats": opponent_advanced_stats,
            "ai_recommendations": ai_recommendations,
            "generated_at": datetime.now().isoformat()
        }


_match_analysis_service = None

def get_match_analysis_service() -> MatchAnalysisService:
    """Get singleton instance of match analysis service"""
    global _match_analysis_service
    if _match_analysis_service is None:
        _match_analysis_service = MatchAnalysisService()
    return _match_analysis_service
