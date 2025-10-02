from pydantic import BaseModel 
from typing import Optional 
from datetime import datetime 

class OAuthCallbackRequest(BaseModel):
    code: str 
    state: Optional[str] = None 

class SessionRequest(BaseModel):
    access_token: str
    refresh_token: str

class AuthResponse(BaseModel):
    access_token: str 
    refresh_token: str 
    token_type: str = "Bearer"
    expires_in: int 
    user: dict 

class LoginResponse(BaseModel):
    success: bool
    redirect_url: str 

class LogoutResponse(BaseModel):
    success: bool
    message: str = "Logged out successfully" 

class RefreshTokenRequest(BaseModel):
    refresh_token: Optional[str] = None 

class RefreshTokenResponse(BaseModel):
    access_token: str 
    expires_in: int

class SessionResponse(BaseModel):
    success: bool
    message: str = "Session created successfully"
