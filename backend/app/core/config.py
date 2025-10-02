from typing import List 
from pydantic_settings import BaseSettings 
from functools import lru_cache

class Settings(BaseSettings):
    # --- App --- 
    APP_NAME: str = "RAG ChatBot"
    ENV: str = "development"
    DEBUG: bool = True 
    # --- URLs --- 
    BACKEND_URL: str 
    FRONTEND_URL: str 
    # --- Supabase --- 
    SUPABASE_URL: str 
    SUPABASE_ANON_KEY: str 
    SUPABASE_SERVICE_KEY: str 
    # --- Security --- 
    SESSION_SECRET: str 
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # --- Cookies --- 
    COOKIE_DOMAIN: str = "localhost"
    COOKIE_SECURE: bool = False 
    COOKIE_SAMESITE: str = "lax"
    COOKIE_HTTPONLY: bool = True 
    # --- CORS --- 
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000"

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENV == "development"
    
    @property 
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]
    
    @property
    def supabase_jwks_url(self) -> str:
        return f"{self.SUPABASE_URL}/auth/v1/keys"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()