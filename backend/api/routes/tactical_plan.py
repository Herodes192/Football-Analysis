"""
Tactical Plan API - AI recommendations with Redis caching
"""
from fastapi import APIRouter, HTTPException
from services.match_analysis_service import MatchAnalysisService
from services.cache_service import get_cache_service

router = APIRouter(prefix="/tactical-plan", tags=["Tactical Plan"])

@router.get("/{opponent_id}")
async def get_tactical_plan(opponent_id: str, opponent_name: str):
    """
    Get AI-powered tactical plan with embedded statistical evidence
    
    🔄 CACHED: Results cached for 24 hours to prevent API token waste
    
    This endpoint provides coaching recommendations separated from raw statistics.
    Stats are included as evidence to support the AI recommendations.
    """
    # Check cache first
    cache = get_cache_service()
    cache_key = f"{opponent_id}_{opponent_name}"
    
    cached_data = await cache.get("tactical_plan", cache_key)
    if cached_data:
        # Return cached data with indicator
        cached_data["data_source"] = "cache"
        cached_data["cache_info"] = "Tactical plan from cache (24h TTL)"
        return cached_data
    
    # Cache miss - generate from API
    try:
        analysis_service = MatchAnalysisService()
        
        # Get full analysis
        full_analysis = await analysis_service.analyze_match(opponent_id, opponent_name)
        
        # Extract relevant sections
        ai_recs = full_analysis.get('ai_recommendations', {})
        advanced_stats = full_analysis.get('opponent_advanced_stats', {})
        opponent_form = full_analysis.get('opponent_form', {})
        
        # Build tactical plan with embedded stats as evidence
        result = {
            "opponent": opponent_name,
            "tactical_plan": {
                "formation_recommendations": {
                    "suggested_changes": ai_recs.get('formation_changes', []),
                    "supporting_evidence": {
                        "opponent_shape": advanced_stats.get('team_shape', {}),
                        "recent_form": opponent_form.get('form_summary', {})
                    }
                },
                "pressing_strategy": {
                    "recommendation": ai_recs.get('pressing_adjustments', {}),
                    "supporting_evidence": {
                        "opponent_pressing": advanced_stats.get('pressing_structure', {}),
                        "possession_stats": advanced_stats.get('possession_control', {})
                    }
                },
                "target_zones": {
                    "priority_zones": ai_recs.get('target_zones', []),
                    "supporting_evidence": {
                        "defensive_vulnerabilities": advanced_stats.get('defensive_actions', {}),
                        "weak_areas": [w for w in ai_recs.get('exploit_weaknesses', []) if w.get('severity') in ['CRITICAL', 'HIGH']]
                    }
                },
                "player_roles": {
                    "role_changes": ai_recs.get('player_role_changes', []),
                    "supporting_evidence": {
                        "opponent_width": advanced_stats.get('team_shape', {}).get('width_usage'),
                        "transition_speed": advanced_stats.get('transitions', {})
                    }
                },
                "game_phases": {
                    "in_possession": ai_recs.get('in_possession_focus', 'Build from the back, control tempo'),
                    "out_possession": ai_recs.get('out_possession_focus', 'Compact defensive block'),
                    "transitions": ai_recs.get('transition_strategy', 'Quick counter-attacks'),
                    "supporting_evidence": {
                        "goal_timing": opponent_form.get('goals_by_period', {}),
                        "defensive_timing": opponent_form.get('conceded_by_period', {})
                    }
                },
                "substitution_strategy": {
                    "recommendations": ai_recs.get('substitution_strategy', []),
                    "supporting_evidence": {
                        "late_game_performance": opponent_form.get('late_game_record', {})
                    }
                },
                "critical_weaknesses": ai_recs.get('exploit_weaknesses', [])
            },
            "ai_confidence": ai_recs.get('ai_confidence', {}),
            "generated_at": full_analysis.get('generated_at'),
            "data_source": "api",
            "cache_info": "Fresh tactical plan from API (cached for 24h)"
        }
        
        # Cache the result for 24 hours
        await cache.set("tactical_plan", cache_key, result)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating tactical plan: {str(e)}")
