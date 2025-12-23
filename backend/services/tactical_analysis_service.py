"""
Tactical Analysis Service
Analyzes opponent tactical patterns and generates recommendations
"""
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np

from utils.logger import setup_logger

logger = setup_logger(__name__)


class TacticalAnalysisService:
    """Service for analyzing tactical patterns and generating recommendations"""
    
    def analyze_opponent(self, matches: List[Dict]) -> Dict:
        """
        Analyze opponent's tactical tendencies based on recent matches
        
        Args:
            matches: List of match data dictionaries
            
        Returns:
            Dictionary containing tactical analysis
        """
        if not matches:
            logger.warning("No matches provided for analysis")
            return self._get_default_analysis()
        
        analysis = {
            "formations": self._analyze_formations(matches),
            "playing_style": self._analyze_playing_style(matches),
            "strengths": self._identify_strengths(matches),
            "weaknesses": self._identify_weaknesses(matches),
            "patterns": self._analyze_patterns(matches),
            "performance": self._analyze_performance(matches),
            "confidence_score": self._calculate_confidence(len(matches))
        }
        
        return analysis
    
    def _analyze_formations(self, matches: List[Dict]) -> Dict:
        """Analyze formation usage patterns"""
        formations = {}
        
        for match in matches:
            formation = match.get("formation", "Unknown")
            formations[formation] = formations.get(formation, 0) + 1
        
        total = len(matches)
        formation_percentages = {
            form: (count / total) * 100 
            for form, count in formations.items()
        }
        
        primary = max(formation_percentages, key=formation_percentages.get) if formations else "Unknown"
        
        return {
            "primary_formation": primary,
            "formation_distribution": formation_percentages,
            "formation_flexibility": len(formations)  # Number of different formations used
        }
    
    def _analyze_playing_style(self, matches: List[Dict]) -> Dict:
        """Analyze team's playing style metrics"""
        possessions = []
        shots = []
        passes = []
        
        for match in matches:
            stats = match.get("statistics", {})
            if stats.get("possession"):
                possessions.append(float(stats["possession"]))
            if stats.get("shots"):
                shots.append(int(stats["shots"]))
            if stats.get("passes"):
                passes.append(int(stats["passes"]))
        
        return {
            "avg_possession": np.mean(possessions) if possessions else 50.0,
            "avg_shots": np.mean(shots) if shots else 10.0,
            "avg_passes": np.mean(passes) if passes else 300.0,
            "possession_style": "possession-based" if np.mean(possessions) > 55 else "direct",
            "attacking_intensity": "high" if np.mean(shots) > 15 else "moderate"
        }
    
    def _identify_strengths(self, matches: List[Dict]) -> List[str]:
        """Identify team's key strengths"""
        strengths = []
        
        # Analyze various metrics to identify strengths
        avg_goals = np.mean([m.get("goals_scored", 0) for m in matches])
        avg_possession = np.mean([float(m.get("statistics", {}).get("possession", 50)) for m in matches])
        avg_shots_on_target = np.mean([m.get("statistics", {}).get("shots_on_target", 0) for m in matches])
        
        if avg_goals > 1.5:
            strengths.append("clinical_finishing")
        if avg_possession > 55:
            strengths.append("possession_control")
        if avg_shots_on_target > 5:
            strengths.append("shot_accuracy")
        
        return strengths if strengths else ["balanced_play"]
    
    def _identify_weaknesses(self, matches: List[Dict]) -> List[str]:
        """Identify team's key weaknesses"""
        weaknesses = []
        
        # Analyze defensive metrics
        avg_goals_conceded = np.mean([m.get("goals_conceded", 0) for m in matches])
        clean_sheets = sum(1 for m in matches if m.get("goals_conceded", 0) == 0)
        
        if avg_goals_conceded > 1.5:
            weaknesses.append("defensive_vulnerability")
        if clean_sheets / len(matches) < 0.3:
            weaknesses.append("poor_defensive_consistency")
        
        return weaknesses if weaknesses else ["no_clear_weakness"]
    
    def _analyze_patterns(self, matches: List[Dict]) -> Dict:
        """Analyze tactical patterns"""
        home_results = [m for m in matches if m.get("is_home")]
        away_results = [m for m in matches if not m.get("is_home")]
        
        return {
            "home_away_difference": {
                "home_avg_goals": np.mean([m.get("goals_scored", 0) for m in home_results]) if home_results else 0,
                "away_avg_goals": np.mean([m.get("goals_scored", 0) for m in away_results]) if away_results else 0
            },
            "consistency": self._calculate_consistency(matches)
        }
    
    def _analyze_performance(self, matches: List[Dict]) -> Dict:
        """Analyze overall performance metrics"""
        wins = sum(1 for m in matches if m.get("result") == "W")
        draws = sum(1 for m in matches if m.get("result") == "D")
        losses = sum(1 for m in matches if m.get("result") == "L")
        
        return {
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate": (wins / len(matches)) * 100 if matches else 0,
            "form": self._calculate_form(matches[-5:] if len(matches) >= 5 else matches)
        }
    
    def _calculate_consistency(self, matches: List[Dict]) -> str:
        """Calculate team consistency level"""
        goals_scored = [m.get("goals_scored", 0) for m in matches]
        std_dev = np.std(goals_scored) if goals_scored else 0
        
        if std_dev < 0.8:
            return "very_consistent"
        elif std_dev < 1.2:
            return "consistent"
        else:
            return "inconsistent"
    
    def _calculate_form(self, recent_matches: List[Dict]) -> str:
        """Calculate current form"""
        points = sum(3 if m.get("result") == "W" else 1 if m.get("result") == "D" else 0 
                    for m in recent_matches)
        max_points = len(recent_matches) * 3
        
        form_percentage = (points / max_points) * 100 if max_points > 0 else 0
        
        if form_percentage >= 70:
            return "excellent"
        elif form_percentage >= 50:
            return "good"
        elif form_percentage >= 30:
            return "moderate"
        else:
            return "poor"
    
    def _calculate_confidence(self, sample_size: int) -> float:
        """Calculate confidence score based on sample size"""
        if sample_size >= 10:
            return 0.9
        elif sample_size >= 5:
            return 0.7
        elif sample_size >= 3:
            return 0.5
        else:
            return 0.3
    
    def _get_default_analysis(self) -> Dict:
        """Return default analysis when no data available"""
        return {
            "formations": {"primary_formation": "Unknown", "formation_distribution": {}, "formation_flexibility": 0},
            "playing_style": {"avg_possession": 50.0, "possession_style": "unknown", "attacking_intensity": "unknown"},
            "strengths": ["insufficient_data"],
            "weaknesses": ["insufficient_data"],
            "patterns": {"home_away_difference": {}, "consistency": "unknown"},
            "performance": {"wins": 0, "draws": 0, "losses": 0, "win_rate": 0, "form": "unknown"},
            "confidence_score": 0.0
        }
    
    def generate_recommendations(self, opponent_analysis: Dict, gil_vicente_formation: str = "4-3-3") -> Dict:
        """
        Generate tactical recommendations for Gil Vicente
        
        Args:
            opponent_analysis: Tactical analysis of the opponent
            gil_vicente_formation: Gil Vicente's preferred formation
            
        Returns:
            Dictionary with tactical recommendations
        """
        recommendations = {
            "recommended_formation": self._recommend_formation(opponent_analysis, gil_vicente_formation),
            "pressing_strategy": self._recommend_pressing(opponent_analysis),
            "key_zones_to_exploit": self._identify_zones_to_exploit(opponent_analysis),
            "defensive_focus": self._recommend_defensive_focus(opponent_analysis),
            "risk_factors": self._identify_risk_factors(opponent_analysis),
            "tactical_adjustments": self._suggest_tactical_adjustments(opponent_analysis)
        }
        
        return recommendations
    
    def _recommend_formation(self, analysis: Dict, default: str) -> str:
        """Recommend formation based on opponent analysis"""
        opponent_formation = analysis.get("formations", {}).get("primary_formation", "Unknown")
        opponent_strengths = analysis.get("strengths", [])
        
        # Rule-based formation recommendation logic
        if "possession_control" in opponent_strengths:
            return "4-3-3"  # Match possession with midfield control
        elif opponent_formation in ["3-5-2", "5-3-2"]:
            return "4-3-3"  # Wide play against 3-back systems
        elif "clinical_finishing" in opponent_strengths:
            return "4-5-1"  # More defensive setup
        
        return default
    
    def _recommend_pressing(self, analysis: Dict) -> Dict:
        """Recommend pressing strategy"""
        playing_style = analysis.get("playing_style", {})
        possession = playing_style.get("avg_possession", 50)
        
        if possession > 60:
            return {
                "intensity": "high",
                "description": "Opponent likes possession - press high to disrupt build-up"
            }
        elif possession < 45:
            return {
                "intensity": "mid-block",
                "description": "Opponent plays direct - sit deeper and control transitions"
            }
        else:
            return {
                "intensity": "moderate",
                "description": "Balanced pressing approach - adapt based on game state"
            }
    
    def _identify_zones_to_exploit(self, analysis: Dict) -> List[str]:
        """Identify key zones to exploit"""
        weaknesses = analysis.get("weaknesses", [])
        zones = []
        
        if "defensive_vulnerability" in weaknesses:
            zones.append("central_penetration")
        if "poor_defensive_consistency" in weaknesses:
            zones.append("sustained_pressure")
        
        zones.append("wide_areas")  # Default recommendation
        return zones
    
    def _recommend_defensive_focus(self, analysis: Dict) -> Dict:
        """Recommend defensive focus areas"""
        strengths = analysis.get("strengths", [])
        
        if "clinical_finishing" in strengths:
            return {
                "priority": "limit_chances",
                "description": "Opponent is clinical - minimize clear goal-scoring opportunities"
            }
        elif "shot_accuracy" in strengths:
            return {
                "priority": "block_shots",
                "description": "Opponent accurate with shots - force wide angles and block attempts"
            }
        
        return {
            "priority": "maintain_shape",
            "description": "Keep defensive organization and limit spaces"
        }
    
    def _identify_risk_factors(self, analysis: Dict) -> List[str]:
        """Identify key risk factors"""
        risks = []
        strengths = analysis.get("strengths", [])
        performance = analysis.get("performance", {})
        
        if "clinical_finishing" in strengths:
            risks.append("High conversion rate - must limit shots")
        
        if performance.get("form") in ["excellent", "good"]:
            risks.append("Opponent in good form - expect strong performance")
        
        if not risks:
            risks.append("Standard tactical awareness required")
        
        return risks
    
    def _suggest_tactical_adjustments(self, analysis: Dict) -> List[str]:
        """Suggest specific tactical adjustments"""
        adjustments = []
        playing_style = analysis.get("playing_style", {})
        
        if playing_style.get("possession_style") == "possession-based":
            adjustments.append("Stay compact when defending - don't chase the ball")
        
        if playing_style.get("attacking_intensity") == "high":
            adjustments.append("Be ready for quick transitions - counter-attack opportunities")
        
        adjustments.append("Monitor set-piece situations - potential scoring opportunities")
        
        return adjustments


# Singleton instance
_tactical_analysis_service = None

def get_tactical_analysis_service() -> TacticalAnalysisService:
    """Get singleton instance of TacticalAnalysisService"""
    global _tactical_analysis_service
    if _tactical_analysis_service is None:
        _tactical_analysis_service = TacticalAnalysisService()
    return _tactical_analysis_service
