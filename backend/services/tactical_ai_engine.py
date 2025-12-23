"""
Tactical AI Engine - Match-to-Tactic Recommendation Model
Generates AI-powered tactical recommendations based on match stats
"""
from typing import Dict, List


class TacticalAIEngine:
    """
    AI-powered tactical recommendation system
    Analyzes opponent stats and generates actionable tactical advice
    """
    
    def generate_recommendations(self, opponent_stats: Dict, gil_stats: Dict) -> Dict:
        """
        Generate comprehensive tactical recommendations
        Based on AI analysis of opponent weaknesses and Gil Vicente strengths
        """
        
        recommendations = {
            "formation_changes": self._recommend_formation(opponent_stats),
            "pressing_adjustments": self._recommend_pressing(opponent_stats),
            "player_role_changes": self._recommend_player_roles(opponent_stats),
            "target_zones": self._identify_target_zones(opponent_stats),
            "substitution_timing": self._recommend_substitutions(opponent_stats),
            "in_game_switches": self._recommend_in_game_switches(opponent_stats),
            "exploit_weaknesses": self._identify_exploitable_weaknesses(opponent_stats),
            "ai_confidence": self._calculate_confidence(opponent_stats)
        }
        
        return recommendations
    
    def _recommend_formation(self, stats: Dict) -> Dict:
        """AI recommendation for formation based on opponent patterns"""
        pressing = stats.get('pressing_structure', {})
        defense = stats.get('defensive_actions', {})
        shape = stats.get('team_shape', {})
        
        ppda = pressing.get('PPDA', 12)
        defensive_rating = defense.get('defensive_rating', 'Average')
        
        recommendations = []
        
        # High press opponents → go direct
        if ppda < 10:
            recommendations.append({
                "formation": "4-4-2 Diamond",
                "reason": "Opponent presses high - bypass with direct play through diamond",
                "priority": "HIGH"
            })
        
        # Vulnerable defense → attack
        if defensive_rating == "Vulnerable":
            recommendations.append({
                "formation": "4-3-3 Attack",
                "reason": "Weak defense detected - use width and pace to overload",
                "priority": "CRITICAL"
            })
        
        # Compact shape → need width
        if shape.get('team_compactness') == 'Narrow':
            recommendations.append({
                "formation": "3-5-2 Wide",
                "reason": "Opponent plays narrow - exploit flanks with wingbacks",
                "priority": "MEDIUM"
            })
        
        return {
            "recommendations": recommendations if recommendations else [{"formation": "4-2-3-1", "reason": "Balanced approach", "priority": "MEDIUM"}],
            "current_formation": "4-2-3-1"
        }
    
    def _recommend_pressing(self, stats: Dict) -> Dict:
        """AI pressing height and intensity adjustments"""
        pressing = stats.get('pressing_structure', {})
        possession = stats.get('possession_control', {})
        
        ppda = pressing.get('PPDA', 12)
        pass_accuracy = possession.get('pass_accuracy', 75)
        
        recommendations = []
        
        if pass_accuracy < 75:
            recommendations.append({
                "adjustment": "HIGH PRESS",
                "target_line": "50-60m from own goal",
                "reason": f"Low pass accuracy ({pass_accuracy}%) - press high to force errors",
                "priority": "CRITICAL"
            })
        
        if ppda > 14:
            recommendations.append({
                "adjustment": "MID-BLOCK",
                "target_line": "35-45m from own goal",
                "reason": "Opponent doesn't press - control midfield and counter",
                "priority": "MEDIUM"
            })
        
        return {
            "pressing_recommendations": recommendations if recommendations else [{"adjustment": "STANDARD", "target_line": "40-50m", "reason": "Balanced approach", "priority": "LOW"}]
        }
    
    def _recommend_player_roles(self, stats: Dict) -> List[Dict]:
        """Specific player role changes"""
        shape = stats.get('team_shape', {})
        pressing = stats.get('pressing_structure', {})
        set_pieces = stats.get('set_pieces', {})
        
        roles = []
        
        # Inverted fullbacks if opponent uses width
        if shape.get('width_usage') == 'Wide flanks exploited':
            roles.append({
                "position": "Fullbacks",
                "role_change": "Inverted Fullbacks → Tuck inside to block central penetration",
                "reason": "Opponent exploits flanks - need central cover"
            })
        else:
            roles.append({
                "position": "Fullbacks",
                "role_change": "Overlapping Fullbacks → Push high and wide",
                "reason": "Opponent doesn't use width - exploit space"
            })
        
        # False 9 if high defensive line
        if shape.get('defensive_line_height', 40) > 48:
            roles.append({
                "position": "Striker",
                "role_change": "False 9 → Drop deep to drag defenders",
                "reason": "High defensive line - create space for runners"
            })
        
        # Target man for set pieces if weak
        if set_pieces.get('defensive', {}).get('set_piece_weakness') == 'High':
            roles.append({
                "position": "Striker",
                "role_change": "Target Man → Dominant aerial presence for set pieces",
                "reason": "Opponent weak on set pieces - exploit aerially"
            })
        
        return roles
    
    def _identify_target_zones(self, stats: Dict) -> Dict:
        """AI-detected weak zones to attack"""
        pressing = stats.get('pressing_structure', {})
        shape = stats.get('team_shape', {})
        transitions = stats.get('transitions', {})
        
        target_zones = []
        
        # Half-spaces if compact
        if shape.get('team_compactness') == 'Narrow':
            target_zones.append({
                "zone": "Half-Spaces (channels between center and flanks)",
                "attack_method": "Inverted wingers cutting inside",
                "priority": "CRITICAL",
                "expected_outcome": "1v1 situations in dangerous areas"
            })
        
        # Wide areas if narrow
        if shape.get('width_usage') == 'Central focus':
            target_zones.append({
                "zone": "Wide Flanks",
                "attack_method": "Overlap with fullbacks and wingers",
                "priority": "HIGH",
                "expected_outcome": "Cross opportunities and cutbacks"
            })
        
        # Behind defense if high line
        if shape.get('defensive_line_height', 40) > 48:
            target_zones.append({
                "zone": "Space Behind Defensive Line",
                "attack_method": "Through balls and runs in behind",
                "priority": "CRITICAL",
                "expected_outcome": "1v1 with goalkeeper"
            })
        
        # Transition spaces if slow recovery
        if transitions.get('defensive_transition', {}).get('recovery_time_after_loss') == 'Slow (>5s)':
            target_zones.append({
                "zone": "Counter-Attack Spaces",
                "attack_method": "Quick transitions after recovery",
                "priority": "HIGH",
                "expected_outcome": "Numerical superiority in attack"
            })
        
        return {
            "priority_zones": target_zones,
            "zone_heatmap_recommendation": "Focus on: " + ", ".join([z['zone'] for z in target_zones[:2]])
        }
    
    def _recommend_substitutions(self, stats: Dict) -> Dict:
        """AI-driven substitution timing recommendations"""
        context = stats.get('context', {})
        pressing = stats.get('pressing_structure', {})
        
        subs = []
        
        # Fresh legs if opponent tires late
        if context.get('fatigue_indicators') == 'High':
            subs.append({
                "timing": "60-65 minutes",
                "type": "Fresh attackers",
                "reason": "Opponent shows fatigue - exploit with pace in final third"
            })
        
        # Defensive reinforcement if losing
        if pressing.get('pressing_intensity') == 'High':
            subs.append({
                "timing": "70-75 minutes",
                "type": "Defensive midfielder",
                "reason": "High press fatigues them - control midfield late"
            })
        
        return {
            "substitution_recommendations": subs if subs else [{"timing": "70 minutes", "type": "Standard rotation", "reason": "Maintain freshness"}]
        }
    
    def _recommend_in_game_switches(self, stats: Dict) -> List[Dict]:
        """Real-time tactical switches during the match"""
        pressing = stats.get('pressing_structure', {})
        possession = stats.get('possession_control', {})
        
        switches = []
        
        if possession.get('possession_percent', 50) < 40:
            switches.append({
                "trigger": "If possession < 40%",
                "switch": "Shift from 4-3-3 → 5-3-2",
                "timing": "Immediately",
                "reason": "Stabilize possession with extra center-back"
            })
        
        if pressing.get('PPDA', 12) < 9:
            switches.append({
                "trigger": "If opponent presses aggressively",
                "switch": "Direct long balls → Target striker",
                "timing": "When pressed",
                "reason": "Bypass press with aerial route"
            })
        
        return switches if switches else [{"trigger": "Standard", "switch": "No immediate changes", "timing": "Monitor", "reason": "Maintain current approach"}]
    
    def _identify_exploitable_weaknesses(self, stats: Dict) -> List[Dict]:
        """AI-detected weaknesses with exploitation strategies"""
        weaknesses = []
        
        # Analyze all stat categories
        pressing = stats.get('pressing_structure', {})
        defense = stats.get('defensive_actions', {})
        set_pieces = stats.get('set_pieces', {})
        transitions = stats.get('transitions', {})
        
        # Weak press
        if pressing.get('PPDA', 12) > 15:
            weaknesses.append({
                "weakness": "No Pressing Structure",
                "severity": "CRITICAL",
                "exploitation": "Build from back → Control possession → Patient build-up",
                "expected_impact": "70%+ possession, control tempo"
            })
        
        # Poor defensive transitions
        if transitions.get('defensive_transition', {}).get('rest_defense_quality') == 'Poor':
            weaknesses.append({
                "weakness": "Slow Defensive Transitions",
                "severity": "HIGH",
                "exploitation": "Win ball → Immediate vertical pass → Exploit space",
                "expected_impact": "2-3 clear counter-attack chances"
            })
        
        # Set piece weakness
        if set_pieces.get('defensive', {}).get('set_piece_weakness') == 'High':
            weaknesses.append({
                "weakness": "Set Piece Defending",
                "severity": "CRITICAL",
                "exploitation": "Target tall players → Practice corner routines",
                "expected_impact": "1+ goal from set pieces"
            })
        
        # Low tackle success
        if defense.get('tackle_success_rate', 70) < 60:
            weaknesses.append({
                "weakness": "Poor Tackling",
                "severity": "MEDIUM",
                "exploitation": "Dribble at defenders → Draw fouls in dangerous areas",
                "expected_impact": "Free-kicks near box, potential penalties"
            })
        
        return weaknesses
    
    def _calculate_confidence(self, stats: Dict) -> Dict:
        """AI confidence levels in recommendations"""
        # Calculate based on data quality and patterns
        pressing = stats.get('pressing_structure', {})
        defense = stats.get('defensive_actions', {})
        
        confidence_score = 75  # Base
        
        # High confidence if clear patterns
        if pressing.get('PPDA', 12) > 15 or pressing.get('PPDA', 12) < 9:
            confidence_score += 10
        
        if defense.get('defensive_rating') in ['Vulnerable', 'Solid']:
            confidence_score += 10
        
        return {
            "overall_confidence": min(95, confidence_score),
            "recommendation_reliability": "HIGH" if confidence_score > 80 else "MEDIUM",
            "data_quality": "Good - based on last match analysis"
        }


_tactical_ai_engine = None

def get_tactical_ai_engine():
    """Get singleton instance"""
    global _tactical_ai_engine
    if _tactical_ai_engine is None:
        _tactical_ai_engine = TacticalAIEngine()
    return _tactical_ai_engine
