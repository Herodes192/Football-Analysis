"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Gil Vicente Tactical Intelligence Platform"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/gil_vicente_tactical"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis Cache
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    CACHE_TTL: int = 3600  # 1 hour
    
    # Football API Configuration
    FOOTBALL_API_KEY: str = "ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168"
    FOOTBALL_API_BACKUP_KEY: str = "0783b704d5msh4c7f1c835680fccp1bdf77jsn28306145b1f3"
    FOOTBALL_API_BASE_URL: str = "https://free-api-live-football-data.p.rapidapi.com"
    FOOTBALL_API_RATE_LIMIT: int = 100  # requests per period
    
    # Gil Vicente Configuration
    GIL_VICENTE_TEAM_ID: int = 9764  # Free API team ID
    GIL_VICENTE_LEAGUE_ID: int = 61  # Liga Portugal
    OPPONENT_MATCH_HISTORY_LIMIT: int = 10
    
    # CORS - Allow all origins in development
    CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
