from pydantic import BaseModel, EmailStr 
from typing import Optional 
from datetime import datetime 

class User(BaseModel):
    id: str 
    email: EmailStr 
    name: Optional[str] = None 
    avatar_url: Optional[str] = None 
    provider: Optional[str] = None 
    created_at: Optional[datetime] = None 
    role: str = "user"

    @classmethod
    def from_supabase(cls, user_data: dict ) -> "User":
        """
            Create User from Supabase response 
        """
        return cls(
            id=user_data.get("id"),
            email=user_data.get("email"),
            name=user_data.get("user_metadata", {}).get("full_name"),
            avatar_url=user_data.get("user_metadata", {}).get("avatar_url"),
            provider=user_data.get("app_metadata", {}).get("provider"),
            created_at=user_data.get("created_at"),
            role=user_data.get("role", "user")
        )

class UserResponse(BaseModel):
    user: User 
