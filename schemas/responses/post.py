from datetime import datetime
from pydantic import BaseModel
from .user import UserResponse

class PostResponse(BaseModel):
    """Post response schema"""
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    author: UserResponse  # Nested user data

    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    """Paginated post response"""
    items: list[PostResponse]
    total: int
    page: int
    per_page: int