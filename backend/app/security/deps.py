from typing import Optional
from fastapi import Depends, Request, HTTPException, status
from app.schemas.user import User
from app.security.jwks import jwks_verifier
from app.core.exceptions import AuthException

async def get_token_from_request(request: Request) -> Optional[str]:
    """
    Extract token from cookie or Authorization header
    
    """
    # --- Try cookie first ---
    token = request.cookies.get("sb-access-token")
    if token:
        return token
    
    # --- Try Authorization header --- 
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    
    return None

async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(get_token_from_request)
) -> User:
    """
        Get current authenticated user
    """
    if not token:
        raise AuthException("Not authenticated")
    
    try:
        payload = await jwks_verifier.verify_token(token)
        user_data = payload.get("user") or payload
        return User.from_supabase(user_data)
    except Exception as e:
        raise AuthException(str(e))

async def get_optional_user(
    request: Request,
    token: Optional[str] = Depends(get_token_from_request)
) -> Optional[User]:
    """
      Get user if authenticated, None otherwise
    
    """
    if not token:
        return None
    
    try:
        payload = await jwks_verifier.verify_token(token)
        user_data = payload.get("user") or payload
        return User.from_supabase(user_data)
    except:
        return None