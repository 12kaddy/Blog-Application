from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.role import UserRole

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class UserWithTokenResponse(UserResponse):
    """User response with auth tokens"""
    access_token: str | None = None
    refresh_token: str | None = None