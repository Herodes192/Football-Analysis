"""
Centralized API client with automatic fallback to backup key
"""
import httpx
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class FootballAPIClient:
    """
    API client with automatic key rotation on rate limit (429) or auth errors
    """
    
    PRIMARY_KEY = "ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168"
    BACKUP_KEY = "0783b704d5msh4c7f1c835680fccp1bdf77jsn28306145b1f3"
    BASE_URL = "https://free-api-live-football-data.p.rapidapi.com"
    
    def __init__(self):
        self.current_key = self.PRIMARY_KEY
        self.primary_failed = False
        
    def _get_headers(self, api_key: str) -> Dict[str, str]:
        """Generate headers with specified API key"""
        return {
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make GET request with automatic fallback to backup key
        
        Args:
            endpoint: API endpoint (e.g., "/football-get-all-matches-by-league")
            params: Query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            httpx.HTTPError: If both keys fail
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Try primary key first (unless it already failed)
        if not self.primary_failed:
            try:
                logger.info(f"Calling {endpoint} with PRIMARY key")
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(
                        url,
                        headers=self._get_headers(self.PRIMARY_KEY),
                        params=params
                    )
                    
                    if response.status_code == 200:
                        return response.json()
                    
                    # Rate limit or auth error on primary key
                    if response.status_code in [429, 401, 403]:
                        logger.warning(f"Primary key failed with {response.status_code}, switching to backup")
                        self.primary_failed = True
                        # Fall through to backup key
                    else:
                        response.raise_for_status()
                        
            except httpx.HTTPError as e:
                logger.error(f"Primary key error: {e}")
                self.primary_failed = True
                # Fall through to backup key
        
        # Try backup key
        try:
            logger.info(f"Calling {endpoint} with BACKUP key")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    url,
                    headers=self._get_headers(self.BACKUP_KEY),
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Backup key also failed: {e}")
            raise
    
    def reset_primary(self):
        """Reset primary key status (call this periodically, e.g., every hour)"""
        self.primary_failed = False
        logger.info("Primary key status reset")


# Singleton instance
_api_client = None

def get_api_client() -> FootballAPIClient:
    """Get singleton API client instance"""
    global _api_client
    if _api_client is None:
        _api_client = FootballAPIClient()
    return _api_client
