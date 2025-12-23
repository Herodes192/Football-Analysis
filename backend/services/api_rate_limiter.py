"""
API Rate Limiter to track and limit external API calls
Prevents exceeding daily API quota
"""
import redis
from datetime import datetime, timedelta
from typing import Optional
from utils.logger import setup_logger
from config.settings import get_settings

settings = get_settings()
logger = setup_logger(__name__)


class APIRateLimiter:
    """Rate limiter for external API calls with daily quota tracking"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True
        )
        self.daily_limit = getattr(settings, 'FOOTBALL_API_DAILY_LIMIT', 100)
        self.counter_key = "football_api:daily_calls"
        self.last_reset_key = "football_api:last_reset"
    
    def _reset_if_new_day(self):
        """Reset counter if it's a new day"""
        today = datetime.now().date().isoformat()
        last_reset = self.redis_client.get(self.last_reset_key)
        
        if last_reset != today:
            self.redis_client.set(self.counter_key, 0)
            self.redis_client.set(self.last_reset_key, today)
            logger.info(f"API rate limiter reset for new day: {today}")
    
    def can_make_request(self) -> bool:
        """Check if we can make another API request"""
        self._reset_if_new_day()
        
        current_count = int(self.redis_client.get(self.counter_key) or 0)
        
        if current_count >= self.daily_limit:
            logger.warning(f"Daily API limit reached: {current_count}/{self.daily_limit}")
            return False
        
        return True
    
    def increment_counter(self):
        """Increment the API call counter"""
        self._reset_if_new_day()
        new_count = self.redis_client.incr(self.counter_key)
        logger.info(f"API call made. Daily count: {new_count}/{self.daily_limit}")
        return new_count
    
    def get_remaining_calls(self) -> int:
        """Get number of remaining API calls for today"""
        self._reset_if_new_day()
        current_count = int(self.redis_client.get(self.counter_key) or 0)
        return max(0, self.daily_limit - current_count)
    
    def get_usage_stats(self) -> dict:
        """Get usage statistics"""
        self._reset_if_new_day()
        current_count = int(self.redis_client.get(self.counter_key) or 0)
        
        return {
            "daily_limit": self.daily_limit,
            "calls_made": current_count,
            "calls_remaining": max(0, self.daily_limit - current_count),
            "percentage_used": round((current_count / self.daily_limit) * 100, 2),
            "reset_date": datetime.now().date().isoformat()
        }


# Singleton instance
_rate_limiter = None

def get_rate_limiter() -> APIRateLimiter:
    """Get singleton instance of rate limiter"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = APIRateLimiter()
    return _rate_limiter
