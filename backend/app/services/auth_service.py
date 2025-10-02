from typing import Optional
from datetime import timedelta
import httpx
from fastapi import Request, Response
from app.core.config import get_settings
from app.core.exceptions import AuthException, OAuthException, TokenException
from app.security.oauth import OAuthHandler
from app.security.jwks import jwks_verifier
from app.schemas.auth import AuthResponse, LoginResponse, LogoutResponse, RefreshTokenResponse, SessionRequest, SessionResponse
from app.schemas.user import User

settings = get_settings()

class AuthService:
    """
    Authentication service handling OAuth flows, token management, and sessions
    """
    
    def __init__(self):
        self.oauth_handler = OAuthHandler()
        self.supabase_token_url = f"{settings.SUPABASE_URL}/auth/v1/token"
        self.supabase_logout_url = f"{settings.SUPABASE_URL}/auth/v1/logout"
    
    async def initiate_google_login(self, request: Request) -> LoginResponse:
        """
        Simplified: Just build the Supabase OAuth URL
        No session storage needed - Supabase handles state internally
        """
        try:
            authorize_url = self.oauth_handler.build_authorize_url("google")
            
            return LoginResponse(
                success=True,
                redirect_url=authorize_url
            )
            
        except Exception as e:
            raise OAuthException(f"Failed to initiate login: {str(e)}")
    
    async def create_session_from_tokens(
        self,
        response: Response,
        session_data: SessionRequest
    ) -> SessionResponse:
        """
        Accept tokens from frontend after Supabase OAuth completes.
        Verify them and set HttpOnly cookies.
        """
        try:
            # ---  Verify the access token is legitimate ---
            user_data = await jwks_verifier.verify_token(session_data.access_token)
            
            # ---  Create auth response to reuse cookie-setting logic ---
            auth_response = AuthResponse(
                access_token=session_data.access_token,
                refresh_token=session_data.refresh_token,
                token_type="Bearer",
                expires_in=3600, 
                user=user_data
            )
            
            # ---  Set secure cookies ---
            self._set_auth_cookies(response, auth_response)
            
            return SessionResponse(
                success=True,
                message="Session created successfully"
            )
            
        except TokenException:
            raise AuthException("Invalid access token")
        except Exception as e:
            raise AuthException(f"Failed to create session: {str(e)}")
    
    def _set_auth_cookies(self, response: Response, auth_response: AuthResponse):
        """
        Set secure HTTP-only cookies for tokens
        """
        cookie_config = {
            "httponly": settings.COOKIE_HTTPONLY,
            "secure": settings.COOKIE_SECURE,
            "samesite": settings.COOKIE_SAMESITE,
            "domain": settings.COOKIE_DOMAIN if settings.COOKIE_DOMAIN != "localhost" else None,
        }
        
        # --- Access token cookie ---
        response.set_cookie(
            key="sb-access-token",
            value=auth_response.access_token,
            max_age=auth_response.expires_in,
            **cookie_config
        )
        
        # Refresh token cookie (longer lived)
        response.set_cookie(
            key="sb-refresh-token",
            value=auth_response.refresh_token,
            max_age=int(timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS).total_seconds()),
            **cookie_config
        )
    
    async def refresh_access_token(
        self,
        request: Request,
        response: Response
    ) -> RefreshTokenResponse:
        """
        Refresh access token using refresh token from cookies
        """
        try:
            # --- Get refresh token from cookie ---
            refresh_token = request.cookies.get("sb-refresh-token")
            if not refresh_token:
                raise AuthException("No refresh token found")
            
            # --- Call Supabase token endpoint ---
            async with httpx.AsyncClient() as client:
                token_response = await client.post(
                    self.supabase_token_url,
                    json={
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token
                    },
                    headers={
                        "Authorization": f"Bearer {settings.SUPABASE_ANON_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )

                if token_response.status_code != 200:
                    raise AuthException("Token refresh failed")

                data = token_response.json()

                # Update access token cookie
                cookie_config = {
                    "httponly": settings.COOKIE_HTTPONLY,
                    "secure": settings.COOKIE_SECURE,
                    "samesite": settings.COOKIE_SAMESITE,
                    "domain": settings.COOKIE_DOMAIN if settings.COOKIE_DOMAIN != "localhost" else None,
                }
                
                response.set_cookie(
                    key="sb-access-token",
                    value=data["access_token"],
                    max_age=data["expires_in"],
                    **cookie_config
                )
                
                # If new refresh token provided, update it too
                if "refresh_token" in data:
                    response.set_cookie(
                        key="sb-refresh-token",
                        value=data["refresh_token"],
                        max_age=int(timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS).total_seconds()),
                        **cookie_config
                    )
                
                return RefreshTokenResponse(
                    access_token=data["access_token"],
                    expires_in=data["expires_in"]
                )
                
        except httpx.RequestError as e:
            raise AuthException(f"Network error during token refresh: {str(e)}")
    
    async def logout(self, request: Request, response: Response) -> LogoutResponse:
        """
        Logout user by clearing cookies and optionally revoking tokens
        """
        try:
            # --- Get refresh token to revoke it ---
            refresh_token = request.cookies.get("sb-refresh-token")
            
            # --- Optionally call Supabase logout endpoint to revoke tokens ---
            if refresh_token:
                try:
                    async with httpx.AsyncClient() as client:
                        await client.post(
                            self.supabase_logout_url,
                            headers={
                                "Authorization": f"Bearer {refresh_token}"
                            },
                            timeout=5.0
                        )
                except:
                    # Don't fail logout if revocation fails
                    pass
            
            # Clear cookies
            response.delete_cookie(
                key="sb-access-token",
                domain=settings.COOKIE_DOMAIN if settings.COOKIE_DOMAIN != "localhost" else None
            )
            response.delete_cookie(
                key="sb-refresh-token",
                domain=settings.COOKIE_DOMAIN if settings.COOKIE_DOMAIN != "localhost" else None
            )
            
            return LogoutResponse(
                success=True,
                message="Logged out successfully"
            )
            
        except Exception as e:
            # Even if something fails, clear cookies
            response.delete_cookie("sb-access-token")
            response.delete_cookie("sb-refresh-token")
            
            return LogoutResponse(
                success=True,
                message="Logged out successfully"
            )


# Singleton instance
auth_service = AuthService()