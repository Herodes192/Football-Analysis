"""
AI Tactical Recommendation Engine - Match-to-Tactic Model
Automatically generates tactical recommendations based on opponent stats
"""
from typing import Dict, List
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TacticalRecommendationEngine:
    """AI-driven tactical recommendation system"""
    
    def __init__(self):
        self.recommendation_rules = self._initialize_rules()
    
    def _initialize_rules(self) -> Dict:
        """Initialize tactical decision rules (AI model foundation)"""
        return {
            "formation_rules": [
                {
                    "condition": lambda stats: stats.get("possession_control", {}).get("possession_pct", 50) < 45,
                    "recommendation": "4-5-1 Defensive Block",
                    "reason": "Low possession opponent - absorb pressure and counter"
                },
                {
                    "condition": lambda stats: stats.get("pressing_structure", {}).get("PPDA", 12) > 14,
                    "recommendation": "4-3-3 High Press",
                    "reason": "Opponent allows space - press high and force errors"
                },
                {
                    "condition": lambda stats: stats.get("defensive_actions", {}).get("defensive_duels_won_pct", 70) < 60,
                    "recommendation": "4-2-3-1 with Direct Wingers",
                    "reason": "Weak defensive duels - exploit 1v1 situations"
                },
            ],
            
            "pressing_rules": [
                {
                    "condition": lambda stats: stats.get("possession_control", {}).get("pass_accuracy", 75) < 75,
                    "recommendation": "Aggressive High Press",
                    "reason": "Low pass accuracy - force mistakes in buildup"
                },
                {
                    "condition": lambda stats: stats.get("transitions", {}).get("defensive_transition_quality", "") == "Poor",
                    "recommendation": "Immediate Counter-Press",
                    "reason": "Slow defensive transitions - win ball high"
                },
            ],
            
            "attacking_rules": [
                {
                    "condition": lambda stats: stats.get("team_shape", {}).get("width_usage", "") == "Narrow",
                    "recommendation": "Overload Wide Areas",
                    "reason": "Narrow shape - create overloads on flanks"
                },
                {
                    "condition": lambda stats: stats.get("set_pieces", {}).get("defensive_set_piece_rating", "") == "Vulnerable",
                    "recommendation": "Prioritize Set Pieces",
                    "reason": "Weak set-piece defense - prepare corner/free-kick routines"
                },
                {
                    "condition": lambda stats: stats.get("pressing_structure", {}).get("high_turnovers", 0) < 5,
                    "recommendation": "Patient Buildup",
                    "reason": "Strong high press - build patiently from back"
                },
            ],
            
            "defensive_rules": [
                {
                    "condition": lambda stats: stats.get("transitions", {}).get("attacking_transition_speed", "") == "Fast",
                    "recommendation": "Deep Defensive Line",
                    "reason": "Fast transitions - protect space in behind"
                },
                {
                    "condition": lambda stats: stats.get("chance_creation", {}).get("crosses_attempted", 0) > 15,
                    "recommendation": "Zone Defense in Box",
                    "reason": "High crossing frequency - pack the box"
                },
            ]
        }
    
    def generate_recommendations(self, opponent_stats: Dict) -> Dict:
        """Generate AI-powered tactical recommendations"""
        logger.info("Generating tactical recommendations from stats")
        
        recommendations = {
            "formation": self._recommend_formation(opponent_stats),
            "pressing": self._recommend_pressing_strategy(opponent_stats),
            "attacking": self._recommend_attacking_approach(opponent_stats),
            "defensive": self._recommend_defensive_setup(opponent_stats),
            "key_adjustments": self._identify_key_adjustments(opponent_stats),
            "player_roles": self._recommend_player_roles(opponent_stats),
            "in_game_triggers": self._define_in_game_triggers(opponent_stats)
        }
        
        return recommendations
    
    def _recommend_formation(self, stats: Dict) -> Dict:
        """AI recommendation for formation"""
        for rule in self.recommendation_rules["formation_rules"]:
            if rule["condition"](stats):
                return {
                    "formation": rule["recommendation"],
                    "reason": rule["reason"],
                    "confidence": "High"
                }
        
        return {
            "formation": "4-2-3-1 Balanced",
            "reason": "Standard approach - no clear patterns detected",
            "confidence": "Medium"
        }
    
    def _recommend_pressing_strategy(self, stats: Dict) -> Dict:
        """AI recommendation for pressing"""
        recommendations = []
        for rule in self.recommendation_rules["pressing_rules"]:
            if rule["condition"](stats):
                recommendations.append({
                    "strategy": rule["recommendation"],
                    "reason": rule["reason"]
                })
        
        if not recommendations:
            recommendations.append({
                "strategy": "Mid-Block Press",
                "reason": "Standard pressing approach"
            })
        
        return {"strategies": recommendations}
    
    def _recommend_attacking_approach(self, stats: Dict) -> Dict:
        """AI recommendation for attacking"""
        recommendations = []
        for rule in self.recommendation_rules["attacking_rules"]:
            if rule["condition"](stats):
                recommendations.append({
                    "approach": rule["recommendation"],
                    "reason": rule["reason"]
                })
        
        # Add xG-based recommendations
        xg = stats.get("expected_metrics", {}).get("xG", 1.0)
        shots = stats.get("shooting_finishing", {}).get("total_shots", 10)
        
        if shots > 15 and xg < 1.5:
            recommendations.append({
                "approach": "Quality over Quantity",
                "reason": f"High shot volume ({shots}) but low xG ({xg}) - improve shot selection"
            })
        
        return {"approaches": recommendations}
    
    def _recommend_defensive_setup(self, stats: Dict) -> Dict:
        """AI recommendation for defensive setup"""
        recommendations = []
        for rule in self.recommendation_rules["defensive_rules"]:
            if rule["condition"](stats):
                recommendations.append({
                    "setup": rule["recommendation"],
                    "reason": rule["reason"]
                })
        
        return {"setups": recommendations}
    
    def _identify_key_adjustments(self, stats: Dict) -> List[str]:
        """Identify critical tactical adjustments"""
        adjustments = []
        
        # PPDA analysis
        ppda = stats.get("pressing_structure", {}).get("PPDA", 12)
        if ppda > 15:
            adjustments.append("⚠️ CRITICAL: Opponent allows 15+ passes before pressure - PRESS HIGH")
        
        # Possession analysis
        possession = stats.get("possession_control", {}).get("possession_pct", 50)
        if possession < 40:
            adjustments.append("⚡ Opponent dominates possession - focus on transition quality")
        elif possession > 60:
            adjustments.append("⚡ Opponent high possession - stay compact, counter efficiently")
        
        # Defensive vulnerability
        duels_won = stats.get("defensive_actions", {}).get("defensive_duels_won_pct", 70)
        if duels_won < 60:
            adjustments.append("🎯 TARGET: Weak defensive duels ({}%) - attack 1v1 situations".format(duels_won))
        
        # Set piece opportunity
        if stats.get("set_pieces", {}).get("defensive_set_piece_rating", "") == "Vulnerable":
            adjustments.append("🎯 SET PIECE WEAPON: Opponent weak - prioritize corner routines")
        
        return adjustments
    
    def _recommend_player_roles(self, stats: Dict) -> Dict:
        """Recommend specific player roles"""
        roles = {}
        
        # Wingers
        width_usage = stats.get("team_shape", {}).get("width_usage", "")
        if width_usage == "Narrow":
            roles["wingers"] = "Stay wide, stretch play, 1v1 focus"
        else:
            roles["wingers"] = "Inverted roles, cut inside for shots"
        
        # Fullbacks
        crosses = stats.get("chance_creation", {}).get("crosses_attempted", 0)
        if crosses > 15:
            roles["fullbacks"] = "Tuck inside, don't expose flanks"
        else:
            roles["fullbacks"] = "Overlap, provide width in attack"
        
        # Striker
        line_height = stats.get("team_shape", {}).get("defensive_line_height", "")
        if line_height == "Medium-High":
            roles["striker"] = "Run in behind, exploit high line"
        else:
            roles["striker"] = "Hold-up play, link with midfield"
        
        # Midfield
        ppda = stats.get("pressing_structure", {}).get("PPDA", 12)
        if ppda > 14:
            roles["midfield"] = "High energy, win ball quickly"
        else:
            roles["midfield"] = "Control tempo, patient buildup"
        
        return roles
    
    def _define_in_game_triggers(self, stats: Dict) -> List[Dict]:
        """Define when to make tactical changes during match"""
        triggers = []
        
        # Scoreline triggers
        triggers.append({
            "condition": "If winning at 60min",
            "action": "Switch to 4-5-1, protect lead",
            "reason": "Opponent struggles to break down compact defenses"
        })
        
        # Fatigue trigger
        transition_speed = stats.get("transitions", {}).get("attacking_transition_speed", "")
        if transition_speed == "Fast":
            triggers.append({
                "condition": "After 70min",
                "action": "Drop deeper, fresh legs in defense",
                "reason": "Opponent dangerous on counter - protect late"
            })
        
        # Pressing trigger
        press_success = stats.get("pressing_structure", {}).get("press_success_rate", 60)
        if press_success < 60:
            triggers.append({
                "condition": "If losing possession frequently",
                "action": "Reduce press intensity, mid-block",
                "reason": "Low press success rate - conserve energy"
            })
        
        return triggers


_tactical_engine = None

def get_tactical_recommendation_engine() -> TacticalRecommendationEngine:
    """Get singleton instance"""
    global _tactical_engine
    if _tactical_engine is None:
        _tactical_engine = TacticalRecommendationEngine()
    return _tactical_engine
