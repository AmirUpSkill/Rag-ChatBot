from urllib.parse import urlencode
from app.core.config import get_settings

settings = get_settings()

class OAuthHandler:
    @staticmethod
    def build_authorize_url(provider: str) -> str:
        """
        Build OAuth authorize URL - let Supabase handle state and PKCE internally
        """
        params = {
            "provider": provider,
            "redirect_to": f"{settings.FRONTEND_URL}/auth/callback",
        }
        return f"{settings.SUPABASE_URL}/auth/v1/authorize?{urlencode(params)}"
