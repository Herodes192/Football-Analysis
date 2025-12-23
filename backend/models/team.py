"""
Team model
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    api_team_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    logo = Column(String(500))
    country = Column(String(100))
    founded = Column(Integer)
    venue_name = Column(String(255))
    venue_capacity = Column(Integer)
    
    # Metadata
    is_gil_vicente = Column(Integer, default=0)  # 1 if Gil Vicente, 0 otherwise
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    tactical_profiles = relationship("TacticalProfile", back_populates="team")
    
    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"
