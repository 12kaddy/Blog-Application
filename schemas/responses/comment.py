from datetime import datetime
from pydantic import BaseModel
from .user import UserResponse
from .post import PostResponse

class CommentResponse(BaseModel):
    """Comment response schema"""
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime
    author: UserResponse  # Nested user data
    post: PostResponse  # Nested post data (lite version)

    class Config:
        from_attributes = True

class CommentListResponse(BaseModel):
    """Paginated comment response"""
    items: list[CommentResponse]
    total: int
    page: int
    per_page: int