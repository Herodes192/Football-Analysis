"""
Advanced Stats Analyzer - Deep match analytics for tactical intelligence

NOTE: These metrics are heuristic/estimated based on limited match data available
from the upstream API (primarily score + home/away). They are still useful for
relative profiling and tactical reasoning, but should not be treated as ground-truth.
"""

from typing import Dict, List, Optional


class AdvancedStatsAnalyzer:
    """Analyzes advanced match statistics for tactical recommendations"""

    def analyze_last_game(self, team_matches: List[Dict], team_name: str) -> Dict:
        """Analyze opponent's last game with comprehensive statistics."""
        if not team_matches:
            return self._get_empty_stats(team_name)

        last_match = team_matches[-1]
        return self.analyze_game(last_match, team_name)

    def analyze_game(self, match: Dict, team_name: str) -> Dict:
        """Analyze a single match for a given team name."""
        if not match:
            return self._get_empty_stats(team_name)

        home = match.get("home", {}) or {}
        away = match.get("away", {}) or {}
        status = match.get("status", {}) or {}

        is_home = str(home.get("name", "")) == str(team_name)
        # If names don't match (data quality), fall back to "home" when unknown
        if not str(home.get("name", "")) and not str(away.get("name", "")):
            is_home = True

        team_score = home.get("score") if is_home else away.get("score")
        opp_score = away.get("score") if is_home else home.get("score")
        try:
            team_score = int(team_score)
        except Exception:
            team_score = 0
        try:
            opp_score = int(opp_score)
        except Exception:
            opp_score = 0

        opponent_name = away.get("name") if is_home else home.get("name")

        # Calculate all stats from available data
        stats = {
            "estimated": True,
            "match_info": {
                "opponent": opponent_name,
                "score": f"{team_score}-{opp_score}",
                "result": "W" if team_score > opp_score else "L" if team_score < opp_score else "D",
                "location": "Home" if is_home else "Away",
                "date": status.get("utcTime", ""),
            },
            # 1. CORE MATCH STATS
            "possession_control": self._analyze_possession(match, team_score, opp_score, is_home),
            "shooting_finishing": self._analyze_shooting(match, team_score, opp_score, is_home),
            # 2. ADVANCED ATTACKING METRICS
            "expected_metrics": self._calculate_expected_metrics(match, team_score, opp_score),
            "chance_creation": self._analyze_chance_creation(match, team_score, opp_score),
            # 3. DEFENSIVE INTELLIGENCE
            "defensive_actions": self._analyze_defensive_actions(match, team_score, opp_score),
            "pressing_structure": self._analyze_pressing(match, team_score, opp_score),
            # 4. SPATIAL & POSITIONAL DATA
            "team_shape": self._analyze_team_shape(match, is_home),
            # 5. TRANSITION STATS
            "transitions": self._analyze_transitions(match, team_score, opp_score),
            # 6. SET PIECE ANALYTICS
            "set_pieces": self._analyze_set_pieces(match, team_score, opp_score),
            # 7. CONTEXTUAL VARIABLES
            "context": self._analyze_context(match, team_score, opp_score),
        }

        return stats

    def analyze_recent_games(self, team_matches: List[Dict], team_name: str, limit: int = 5) -> List[Dict]:
        """Analyze up to N most recent finished games (expects match objects)."""
        if not team_matches:
            return []

        matches = list(team_matches)
        matches.sort(key=lambda m: (m.get("status", {}) or {}).get("utcTime", ""), reverse=True)
        analyzed = []
        for m in matches[: max(0, int(limit))]:
            analyzed.append(self.analyze_game(m, team_name))
        return analyzed

    def _analyze_possession(self, match: Dict, team_score: int, opp_score: int, is_home: bool) -> Dict:
        """Core possession & control metrics"""
        base_possession = 50
        if is_home:
            base_possession += 5
        if team_score > opp_score:
            base_possession += 10
        elif team_score < opp_score:
            base_possession -= 10

        possession = max(30, min(70, base_possession))

        return {
            "possession_percent": possession,
            "time_in_opponent_half": round(possession * 0.85, 1),
            "pass_accuracy": round(75 + (possession - 50) * 0.3, 1),
            "passes_per_minute": round(8 + (possession / 10), 1),
            "long_balls_attempted": 15 + (5 if possession < 45 else 0),
            "long_balls_completed": 8 + (3 if possession < 45 else 0),
            "tempo_rating": "High" if possession > 55 else "Medium" if possession > 45 else "Low",
            "tactical_insight": self._get_possession_insight(possession, team_score),
        }

    def _analyze_shooting(self, match: Dict, team_score: int, opp_score: int, is_home: bool) -> Dict:
        """Shooting & finishing analysis"""
        total_shots = max(8, team_score * 4 + (6 if is_home else 4))
        shots_on_target = max(2, team_score * 2 + 1)

        return {
            "total_shots": total_shots,
            "shots_on_target": shots_on_target,
            "shot_conversion_rate": round((team_score / total_shots) * 100, 1) if total_shots > 0 else 0,
            "shots_inside_box": round(total_shots * 0.65),
            "shots_outside_box": round(total_shots * 0.35),
            "big_chances_created": max(1, team_score + 1),
            "big_chances_missed": max(0, 3 - team_score) if team_score < 3 else 0,
            "tactical_insight": self._get_shooting_insight(total_shots, team_score),
        }

    def _calculate_expected_metrics(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Expected goals and assists calculations"""
        xg = round(team_score + (0.3 if team_score > opp_score else -0.2), 2)
        xg = max(0.2, xg)

        return {
            "xG": xg,
            "xG_per_shot": round(xg / max(10, team_score * 4), 3),
            "xG_from_open_play": round(xg * 0.75, 2),
            "xG_from_set_pieces": round(xg * 0.25, 2),
            "xA": round(xg * 0.8, 2),
            "performance_rating": "Overperforming"
            if team_score > xg + 0.5
            else "Underperforming"
            if team_score < xg - 0.5
            else "Expected",
        }

    def _analyze_chance_creation(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Chance creation patterns"""
        key_passes = max(5, team_score * 3 + 4)

        return {
            "key_passes": key_passes,
            "progressive_passes": 25 + (team_score * 5),
            "passes_into_final_third": 35 + (team_score * 8),
            "passes_into_penalty_area": 8 + (team_score * 3),
            "crosses_attempted": 12 + (4 if team_score < 2 else 0),
            "crosses_accurate": 3 + (1 if team_score > 1 else 0),
            "cutbacks": 2 + team_score,
            "creation_quality": "High" if key_passes > 12 else "Medium" if key_passes > 7 else "Low",
        }

    def _analyze_defensive_actions(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Defensive metrics and actions"""
        tackles_won = 12 + (opp_score * 2)

        return {
            "tackles_attempted": tackles_won + 4,
            "tackles_won": tackles_won,
            "tackle_success_rate": round((tackles_won / (tackles_won + 4)) * 100, 1),
            "interceptions": 8 + (3 if opp_score < 2 else 0),
            "blocks": 4 + opp_score,
            "clearances": 15 + (opp_score * 3),
            "defensive_duels_won_percent": round(55 + (5 if opp_score < 2 else -5), 1),
            "defensive_rating": "Solid" if opp_score < 2 else "Vulnerable" if opp_score > 2 else "Average",
        }

    def _analyze_pressing(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Pressing intensity and structure"""
        ppda = round(12.5 - (team_score * 1.5) + (opp_score * 1.5), 1)
        ppda = max(6.0, min(18.0, ppda))

        return {
            "PPDA": ppda,
            "pressing_intensity": "High" if ppda < 10 else "Medium" if ppda < 14 else "Low",
            "high_turnovers_won": max(3, 8 - int(ppda / 2)),
            "counter_press_recoveries": max(2, 6 - int(ppda / 3)),
            "pressing_zones": ["High third", "Mid third"] if ppda < 12 else ["Mid third", "Low third"],
            "tactical_insight": self._get_pressing_insight(ppda, opp_score),
        }

    def _analyze_team_shape(self, match: Dict, is_home: bool) -> Dict:
        """Team shape and positioning"""
        return {
            "avg_team_line_height": "High" if is_home else "Medium",
            "defensive_line_height": 45 + (5 if is_home else 0),
            "distance_between_lines": "Compact (15-20m)" if is_home else "Standard (20-25m)",
            "team_compactness": "Narrow" if is_home else "Balanced",
            "width_usage": "Wide flanks exploited" if is_home else "Central focus",
            "formation_detected": "4-2-3-1" if is_home else "4-4-2",
        }

    def _analyze_transitions(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Transition speed and efficiency"""
        return {
            "attacking_transition": {
                "time_recovery_to_shot": "Fast (<10s)" if team_score > 1 else "Medium (10-20s)",
                "passes_per_counter": 3 + (2 if team_score < 2 else 0),
                "direct_attacks": 8 + (team_score * 2),
                "counter_efficiency": "High" if team_score > opp_score else "Low",
            },
            "defensive_transition": {
                "counter_attacks_conceded": 5 + (opp_score * 2),
                "recovery_time_after_loss": "Slow (>5s)" if opp_score > 2 else "Fast (<5s)",
                "fouls_stopping_counters": 3 + opp_score,
                "rest_defense_quality": "Poor" if opp_score > 2 else "Good",
            },
        }

    def _analyze_set_pieces(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Set piece effectiveness"""
        corners = 4 + (team_score * 2)

        return {
            "attacking": {
                "corners_taken": corners,
                "xG_from_corners": round(corners * 0.12, 2),
                "first_contact_success": f"{round((team_score / max(1, corners)) * 100, 1)}%",
                "second_ball_recoveries": max(1, team_score),
                "set_piece_goals": 1 if team_score > 0 and corners > 5 else 0,
            },
            "defensive": {
                "corners_conceded": 3 + (opp_score * 2),
                "marking_type": "Zonal" if opp_score < 2 else "Man-marking",
                "clearances_under_pressure": 8 + (opp_score * 2),
                "shots_conceded_after_set_pieces": max(2, opp_score),
                "set_piece_weakness": "High" if opp_score > 2 else "Low",
            },
        }

    def _analyze_context(self, match: Dict, team_score: int, opp_score: int) -> Dict:
        """Contextual and psychological factors"""
        return {
            "scoreline_state": "Winning" if team_score > opp_score else "Losing" if team_score < opp_score else "Drawing",
            "game_momentum": "Positive" if team_score > opp_score else "Negative",
            "pressure_handling": "Good" if abs(team_score - opp_score) <= 1 else "Poor",
            "fatigue_indicators": "Low" if team_score > opp_score else "High",
            "mental_strength": "Strong" if team_score > 0 else "Weak",
        }

    def _get_possession_insight(self, possession: float, goals: int) -> str:
        if possession > 55 and goals < 2:
            return "High possession + low penetration → needs verticality"
        if possession < 45 and goals > 1:
            return "Low possession + high goals → counter-attacking efficiency"
        return "Balanced possession and output"

    def _get_shooting_insight(self, shots: int, goals: int) -> str:
        if shots > 15 and goals < 2:
            return "Many shots, low conversion → poor shot selection"
        if shots < 10 and goals > 1:
            return "Few shots, good conversion → excellent chance creation"
        return "Standard shooting efficiency"

    def _get_pressing_insight(self, ppda: float, goals_conceded: int) -> str:
        if ppda < 10 and goals_conceded > 2:
            return "Low PPDA + high xG conceded → press is disorganized"
        if ppda < 12 and goals_conceded < 2:
            return "Aggressive press working effectively"
        return "Standard pressing approach"

    def _get_empty_stats(self, team_name: str) -> Dict:
        return {
            "error": "No recent match data available",
            "team_name": team_name,
        }


_advanced_stats_analyzer = None


def get_advanced_stats_analyzer():
    """Get singleton instance"""

    global _advanced_stats_analyzer
    if _advanced_stats_analyzer is None:
        _advanced_stats_analyzer = AdvancedStatsAnalyzer()
    return _advanced_stats_analyzer
