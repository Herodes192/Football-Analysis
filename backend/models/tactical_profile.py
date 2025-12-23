"""
Tactical Profile model - stores analyzed tactical tendencies of teams
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class TacticalProfile(Base):
    __tablename__ = "tactical_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    
    # Formation tendencies
    primary_formation = Column(String(20))
    secondary_formation = Column(String(20))
    formation_frequency = Column(JSON)  # {"4-3-3": 0.6, "4-4-2": 0.3, "3-5-2": 0.1}
    
    # Playing style metrics (0-100 scale)
    possession_style = Column(Float)  # High = possession, Low = direct
    build_up_speed = Column(Float)  # High = fast, Low = slow
    defensive_line_height = Column(Float)  # High = high line, Low = deep
    pressing_intensity = Column(Float)  # High = aggressive, Low = passive
    width_of_attack = Column(Float)  # High = wide, Low = central
    
    # Strengths and weaknesses
    key_strengths = Column(JSON)  # ["counter_attacks", "set_pieces", "wing_play"]
    key_weaknesses = Column(JSON)  # ["defending_crosses", "high_press_vulnerable"]
    
    # Performance patterns
    home_performance_avg = Column(Float)  # Average xG or points at home
    away_performance_avg = Column(Float)
    
    # Tactical patterns (JSON for detailed analysis)
    attacking_patterns = Column(JSON)
    defensive_patterns = Column(JSON)
    
    # Analysis metadata
    matches_analyzed = Column(Integer, default=0)
    last_analysis_date = Column(DateTime)
    confidence_score = Column(Float)  # 0-1 scale
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="tactical_profiles")
    
    def __repr__(self):
        return f"<TacticalProfile(team_id={self.team_id}, formation={self.primary_formation})>"
