from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated

from app.models.role import UserRole

class UserCreateRequest(BaseModel):
    """User registration schema"""
    username: Annotated[str, Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")]
    email: EmailStr
    password: Annotated[str, Field(..., min_length=8, max_length=64)]
    role: UserRole = UserRole.USER

    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        return v

class UserUpdateRequest(BaseModel):
    """User update schema"""
    username: Annotated[str | None, Field(None, min_length=3, max_length=50)]
    email: EmailStr | None = None