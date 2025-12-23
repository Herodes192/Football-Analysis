"""
Match model
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    api_fixture_id = Column(Integer, unique=True, nullable=False, index=True)
    
    # Teams
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    
    # Match details
    match_date = Column(DateTime, nullable=False, index=True)
    venue = Column(String(255))
    referee = Column(String(255))
    status = Column(String(50))  # NS, FT, LIVE, etc.
    
    # Score
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    # Advanced stats
    home_possession = Column(Float)
    away_possession = Column(Float)
    home_shots = Column(Integer)
    away_shots = Column(Integer)
    home_shots_on_target = Column(Integer)
    away_shots_on_target = Column(Integer)
    home_xg = Column(Float)
    away_xg = Column(Float)
    
    # Tactical data (JSON for flexibility)
    home_formation = Column(String(20))
    away_formation = Column(String(20))
    tactical_data = Column(JSON)  # Additional tactical metrics
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    
    def __repr__(self):
        return f"<Match(id={self.id}, home={self.home_team_id} vs away={self.away_team_id})>"
