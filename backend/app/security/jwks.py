import httpx
import jwt
from typing import Dict, Optional
from datetime import datetime, timedelta
from functools import lru_cache
from app.core.config import get_settings
from app.core.exceptions import TokenException

settings = get_settings()

class JWKSVerifier:
    def __init__(self):
        self._jwks_cache = None
        self._cache_time = None
        self._cache_duration = timedelta(hours=1)
    
    async def get_jwks(self) -> Dict:
        """
        Fetch and cache JWKS
        """
        now = datetime.utcnow()
        
        if self._jwks_cache and self._cache_time:
            if now - self._cache_time < self._cache_duration:
                return self._jwks_cache
        
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.supabase_jwks_url)
            response.raise_for_status()
            self._jwks_cache = response.json()
            self._cache_time = now
            
        return self._jwks_cache
    
    async def verify_token(self, token: str) -> Dict:
        """Verify JWT token with JWKS"""
        try:
            # ---  Decode without verification to get kid --- 
            unverified = jwt.get_unverified_header(token)
            kid = unverified.get("kid")
            
            if not kid:
                # Fallback to HS256 with secret
                return jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.JWT_ALGORITHM]
                )
            
            # ---  Get JWKS and find matching key ---
            jwks = await self.get_jwks()
            for key in jwks.get("keys", []):
                if key.get("kid") == kid:
                    # ---  Verify with RS256 ---
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                    return jwt.decode(
                        token,
                        public_key,
                        algorithms=["RS256"],
                        audience="authenticated"
                    )
            
            raise TokenException("No matching key found in JWKS")
            
        except jwt.ExpiredSignatureError:
            raise TokenException("Token has expired")
        except jwt.JWTError as e:
            raise TokenException(f"Invalid token: {str(e)}")

jwks_verifier = JWKSVerifier()