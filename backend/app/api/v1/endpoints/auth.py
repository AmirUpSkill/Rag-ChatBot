from fastapi import APIRouter , Request , Response , Depends , status 
from starlette.responses import RedirectResponse

from app.services.auth_service import auth_service
from app.security.deps import get_current_user 
from app.schemas.user import User
from app.schemas.auth import LogoutResponse , RefreshTokenResponse, SessionRequest, SessionResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/login/google",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def google_login(request: Request):
    """
        Initiate Google OAuth login by redirecting the user to Supabase OAuth.
    """
    login_response = await auth_service.initiate_google_login(request)
    return RedirectResponse(url=login_response.redirect_url)

@router.post("/session", response_model=SessionResponse)
async def create_session(
    response: Response,
    session_data: SessionRequest
):
    """
    Accept tokens from frontend after Supabase OAuth completes.
    Verify them and set HttpOnly cookies.
    """
    return await auth_service.create_session_from_tokens(response, session_data)

@router.get("/me" , response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
        Get the profile of the currently authenticated user.
    """
    return current_user 

@router.post("/logout", response_model=LogoutResponse)
async def logout(request: Request, response: Response):
    """
    Log out the user by clearing their session cookies.
    """
    return await auth_service.logout(request, response)

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(request: Request, response: Response):
    """
    Refresh the access token using the refresh token cookie.
    """
    return await auth_service.refresh_access_token(request, response)
